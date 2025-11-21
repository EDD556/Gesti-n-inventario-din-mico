import os
import datetime
import logging
import reflex as rx
from supabase import create_client, Client
from typing import Optional
import pandas as pd
import io

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_client: Optional[Client] = None
if supabase_url and supabase_key:
    try:
        supabase_client = create_client(supabase_url, supabase_key)
    except Exception as e:
        logging.exception(f"Error initializing Supabase: {e}")
        print(f"Error initializing Supabase: {e}")


class InventoryItem(rx.Base):
    """Model for inventory items."""

    id: int = 0
    sku: str = ""
    descripcion: str = ""
    familia: str = ""
    existencia: int = 0
    fecha: str = ""


class InventoryState(rx.State):
    """State management for the inventory system."""

    items: list[InventoryItem] = []
    search_sku: str = ""
    selected_family: str = "Todas"
    selected_date: str = datetime.date.today().isoformat()
    families: list[str] = ["Todas"]
    is_loading: bool = False
    is_uploading: bool = False
    error_message: str = ""
    success_message: str = ""
    special_families: dict[str, list[str]] = {}
    new_family_name: str = ""
    new_family_skus: str = ""

    @rx.var
    def filtered_items(self) -> list[InventoryItem]:
        """Filter items based on search and selected family."""
        filtered = self.items
        if self.search_sku:
            search_term = self.search_sku.lower()
            filtered = [
                item
                for item in filtered
                if search_term in item.sku.lower()
                or search_term in item.descripcion.lower()
            ]
        if self.selected_family and self.selected_family != "Todas":
            if self.selected_family in self.special_families:
                target_skus = self.special_families[self.selected_family]
                filtered = [item for item in filtered if item.sku in target_skus]
            else:
                filtered = [
                    item for item in filtered if item.familia == self.selected_family
                ]
        return filtered

    @rx.var
    def total_stock(self) -> int:
        """Calculate total stock for filtered items."""
        return sum((item.existencia for item in self.filtered_items))

    @rx.var
    def total_items(self) -> int:
        """Calculate total count of filtered items."""
        return len(self.filtered_items)

    @rx.event
    async def load_data(self):
        """Fetch inventory data from Supabase based on selected date."""
        self.is_loading = True
        self.error_message = ""
        if not supabase_client:
            self.error_message = "Error: Credenciales de Supabase no configuradas."
            self.is_loading = False
            return
        try:
            query = supabase_client.table("inventarios").select("*")
            if self.selected_date:
                query = query.eq("fecha", self.selected_date)
            response = query.execute()
            data = response.data
            self.items = [
                InventoryItem(
                    id=item.get("id", 0),
                    sku=item.get("sku", ""),
                    descripcion=item.get("descripcion", ""),
                    familia=item.get("familia", "Unknown"),
                    existencia=item.get("existencia", 0),
                    fecha=item.get("fecha", ""),
                )
                for item in data
            ]
            unique_fams = sorted(
                list(set((item.familia for item in self.items if item.familia)))
            )
            sf_query = (
                supabase_client.table("familias_especiales").select("*").execute()
            )
            special_fams_data = sf_query.data
            self.special_families = {}
            for sf in special_fams_data:
                fam_id = sf["id"]
                fam_name = sf["nombre_familia"]
                skus_query = (
                    supabase_client.table("familias_skus")
                    .select("sku")
                    .eq("familia_id", fam_id)
                    .execute()
                )
                skus_list = [row["sku"] for row in skus_query.data]
                self.special_families[fam_name] = skus_list
            special_fam_names = sorted(list(self.special_families.keys()))
            self.families = ["Todas"] + special_fam_names + unique_fams
        except Exception as e:
            logging.exception(f"Supabase Fetch Error: {e}")
            self.error_message = f"Error al conectar con base de datos: {str(e)}"
            print(f"Supabase Fetch Error: {e}")
        finally:
            self.is_loading = False

    @rx.event
    def set_date(self, date: str):
        """Update date and reload data."""
        self.selected_date = date
        return InventoryState.load_data

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle Excel file upload."""
        self.is_uploading = True
        self.error_message = ""
        self.success_message = ""
        if not files:
            self.is_uploading = False
            return
        file = files[0]
        upload_data = await file.read()
        try:
            df = pd.read_excel(io.BytesIO(upload_data))
            required_cols = ["sku", "descripcion", "familia", "existencia"]
            df.columns = [c.lower() for c in df.columns]
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                raise ValueError(f"Columnas faltantes en Excel: {', '.join(missing)}")
            records = df[required_cols].to_dict("records")
            today = datetime.date.today().isoformat()
            final_records = []
            for r in records:
                final_records.append(
                    {
                        "sku": str(r["sku"]),
                        "descripcion": str(r["descripcion"]),
                        "familia": str(r["familia"]),
                        "existencia": int(r["existencia"]),
                        "fecha": today,
                    }
                )
            if not supabase_client:
                raise Exception("Supabase client not initialized")
            supabase_client.table("inventarios").delete().eq("fecha", today).execute()
            batch_size = 1000
            for i in range(0, len(final_records), batch_size):
                batch = final_records[i : i + batch_size]
                supabase_client.table("inventarios").insert(batch).execute()
            self.success_message = f"Se cargaron {len(final_records)} productos exitosamente para la fecha {today}."
            yield InventoryState.load_data
        except Exception as e:
            logging.exception(f"Upload Error: {e}")
            self.error_message = f"Error al procesar archivo: {str(e)}"
        finally:
            self.is_uploading = False

    @rx.event
    async def create_special_family(self):
        """Create a new special family."""
        if not self.new_family_name:
            self.error_message = "El nombre de la familia es requerido."
            return
        if not supabase_client:
            self.error_message = "Error de conexión."
            return
        try:
            res = (
                supabase_client.table("familias_especiales")
                .insert({"nombre_familia": self.new_family_name})
                .execute()
            )
            if not res.data:
                raise Exception("No se pudo crear la familia.")
            fam_id = res.data[0]["id"]
            skus = [s.strip() for s in self.new_family_skus.split(",") if s.strip()]
            if skus:
                sku_records = [{"familia_id": fam_id, "sku": s} for s in skus]
                supabase_client.table("familias_skus").insert(sku_records).execute()
            self.new_family_name = ""
            self.new_family_skus = ""
            self.success_message = "Familia especial creada exitosamente."
            yield InventoryState.load_data
        except Exception as e:
            logging.exception(f"Create Family Error: {e}")
            self.error_message = f"Error al crear familia: {str(e)}"