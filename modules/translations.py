# modules/translations.py
# Bilingual support: Polish and English

TRANSLATIONS = {
    "pl": {
        # App title & general
        "app_title": "Wiekowanie Zapasów",
        "app_subtitle": "Analiza wieku zapasów magazynowych",
        "language_label": "Język / Language",
        "sidebar_title": "⚙️ Konfiguracja",

        # Upload section
        "upload_header": "📂 Upload pliku z zapasami",
        "upload_label": "Przeciągnij i upuść plik lub kliknij, aby wybrać",
        "upload_help": "Obsługiwane formaty: .xlsx, .xls, .csv",
        "upload_success": "✅ Plik wczytany poprawnie",
        "preview_header": "👁️ Podgląd danych",
        "rows_loaded": "Wczytano wierszy",
        "cols_loaded": "Kolumn",

        # Header row selection
        "header_row_label": "Wiersz nagłówków",
        "header_row_help": "Wskaż, w którym wierszu znajdują się nagłówki kolumn (domyślnie 1)",
        "header_row_preview": "Podgląd surowych danych (pierwsze 6 wierszy)",
        "header_row_reload": "Wczytaj z wybranym wierszem nagłówków",

        # Aging method
        "method_header": "🔧 Metoda wiekowania",
        "method_label": "Wybierz metodę wiekowania",
        "method_index": "Wiekowanie wg indeksu",
        "method_batch": "Wiekowanie wg indeksu i partii",

        # Aging date
        "date_header": "📅 Data wiekowania",
        "date_label": "Wybierz datę wiekowania",

        # Column mapping
        "mapping_header": "🗂️ Mapowanie kolumn",
        "mapping_desc": "Przypisz kolumny z pliku do wymaganych pól",
        "col_material_index": "Indeks materiałowy *",
        "col_receipt_date": "Data przyjęcia zapasu *",
        "col_material_name": "Nazwa materiału *",
        "col_doc_number": "Numer dokumentu przyjęcia *",
        "col_quantity": "Ilość / stan magazynu *",
        "col_value": "Wartość zapasu (opcjonalne)",
        "col_warehouse": "Magazyn (opcjonalne)",
        "col_batch": "Numer partii *",
        "col_select": "-- Wybierz kolumnę --",
        "col_skip": "-- Pomiń --",

        # Aging buckets
        "buckets_header": "📊 Przedziały wiekowania",
        "buckets_type_label": "Typ przedziałów",
        "buckets_default": "Użyj domyślnych przedziałów",
        "buckets_custom": "Wprowadź własne przedziały",
        "buckets_default_title": "Domyślne przedziały wiekowania",
        "buckets_custom_title": "Własne przedziały wiekowania",
        "bucket_name": "Nazwa przedziału",
        "bucket_from": "Dzień od",
        "bucket_to": "Dzień do",
        "bucket_to_help": "Pozostaw puste dla ostatniego otwartego przedziału",
        "bucket_add": "➕ Dodaj przedział",
        "bucket_remove": "Usuń",
        "bucket_last_unlimited": "Ostatni przedział jest nieograniczony (brak górnej granicy)",
        "bucket_error_title": "Błąd w przedziałach",
        "bucket_error_overlap": "Przedziały wiekowania nakładają się lub są nieprawidłowe!",
        "bucket_error_order": "Zakresy dni muszą być rosnące i nie mogą się nakładać!",
        "bucket_warn_gap": "Ostrzeżenie: wykryto lukę między przedziałami",
        "bucket_error_multi_open": "Tylko ostatni przedział może mieć puste pole 'Dzień do'.",
        "bucket_error_empty_name": "Przedział {n}: nazwa jest pusta.",
        "bucket_error_invalid_from": "Przedział {n}: nieprawidłowy 'Dzień od'.",
        "bucket_error_to_lte_from": "Przedział '{name}': 'Dzień do' musi być większy niż 'Dzień od'.",
        "bucket_error_overlaps": "Przedział '{name}': nakłada się z poprzednim.",
        "bucket_error_none": "Brak zdefiniowanych przedziałów.",
        "bucket_error_only_one_open": "Tylko jeden przedział może być otwarty (bez 'Dzień do').",

        # Calculate
        "calc_button": "🔄 Przelicz wiekowanie",
        "calc_success": "✅ Wiekowanie obliczone pomyślnie!",
        "calc_error": "❌ Błąd podczas obliczania wiekowania",

        # Download
        "download_button": "⬇️ Pobierz wynik Excel",
        "download_generating": "Generowanie pliku Excel...",

        # Dashboard
        "dashboard_header": "📈 Dashboard",
        "kpi_total_qty": "Łączna ilość",
        "kpi_total_value": "Łączna wartość",
        "kpi_materials": "Liczba indeksów",
        "kpi_warehouses": "Liczba magazynów",
        "kpi_above_1y": "Udział pow. 1 roku",
        "kpi_above_2y": "Udział pow. 2 lat",
        "chart_qty_title": "Wiekowanie wg ilości",
        "chart_val_title": "Wiekowanie wg wartości",
        "chart_wh_title": "Wiekowanie wg magazynu",
        "chart_top10_old": "Top 10 najstarszych indeksów",
        "chart_top10_val": "Top 10 pozycji o najwyższej wartości",
        "chart_qty_axis": "Ilość",
        "chart_val_axis": "Wartość",
        "chart_bucket_axis": "Przedział wiekowania",
        "chart_material_axis": "Indeks / Nazwa",
        "chart_wh_axis": "Magazyn",

        # Results tabs
        "tab_dashboard": "📊 Dashboard",
        "tab_detail": "📋 Dane szczegółowe",
        "tab_qty_summary": "📦 Podsumowanie ilościowe",
        "tab_val_summary": "💰 Podsumowanie wartościowe",
        "tab_wh_summary": "🏭 Podsumowanie wg magazynu",
        "tab_batch_summary": "🏷️ Podsumowanie wg partii",
        "tab_validation": "⚠️ Walidacja",

        # Validation
        "validation_header": "Dziennik walidacji",
        "val_row": "Wiersz",
        "val_type": "Typ problemu",
        "val_desc": "Opis",
        "val_severity": "Powaga",
        "val_no_issues": "✅ Brak problemów z walidacją",
        "val_issues_found": "znalezionych problemów",
        "severity_error": "BŁĄD",
        "severity_warning": "OSTRZEŻENIE",
        "severity_info": "INFO",

        # Info messages
        "info_no_value_col": "ℹ️ Kolumna wartości nie została zmapowana — pominięto wiekowanie wartościowe.",
        "info_no_wh_col": "ℹ️ Kolumna magazynu nie została zmapowana — pominięto podsumowanie wg magazynu.",
        "info_batch_required": "⚠️ Przy wiekowaniu wg indeksu i partii, kolumna partii jest wymagana.",

        # Excel sheet names
        "sheet_detail": "Dane_Szczegolowe",
        "sheet_qty": "Wiekowanie_Ilosc",
        "sheet_val": "Wiekowanie_Wartosc",
        "sheet_wh": "Wiekowanie_Magazyn",
        "sheet_batch": "Wiekowanie_Partie",
        "sheet_summary": "Podsumowanie",
        "sheet_validation": "Dziennik_Walidacji",

        # Column names in output
        "out_aging_date": "Data wiekowania",
        "out_age_days": "Wiek (dni)",
        "out_age_months": "Wiek (miesiące)",
        "out_bucket": "Przedział wiekowania",
        "out_method": "Metoda wiekowania",
        "out_validation": "Status walidacji",

        # Default bucket labels
        "bucket_0_3": "0–3 miesiące",
        "bucket_3_6": "3–6 miesięcy",
        "bucket_6_9": "6–9 miesięcy",
        "bucket_9_12": "9–12 miesięcy",
        "bucket_1_2": "1–2 lata",
        "bucket_2plus": "Powyżej 2 lat",

        # Steps/instructions
        "step1": "Krok 1: Wczytaj plik",
        "step2": "Krok 2: Skonfiguruj analizę",
        "step3": "Krok 3: Wyniki",
        "instructions": "Zacznij od wczytania pliku Excel lub CSV z danymi magazynowymi.",
        "error_missing_cols": "Brakuje mapowania wymaganych kolumn: ",
        "error_file_read": "Nie można odczytać pliku. Sprawdź format i spróbuj ponownie.",
        "error_date_col": "Kolumna daty zawiera nieprawidłowe wartości.",
        "ok": "OK",
        "warning": "Ostrzeżenie",
        "total": "Łącznie",
        "mandatory_cols": "Kolumny wymagane",
        "optional_cols": "Kolumny opcjonalne",
        "batch_col_required": "Kolumna partii (wymagana)",
    },
    "en": {
        # App title & general
        "app_title": "Inventory Aging Analyzer",
        "app_subtitle": "Inventory stock age analysis",
        "language_label": "Język / Language",
        "sidebar_title": "⚙️ Configuration",

        # Upload section
        "upload_header": "📂 Upload inventory file",
        "upload_label": "Drag & drop file or click to browse",
        "upload_help": "Supported formats: .xlsx, .xls, .csv",
        "upload_success": "✅ File loaded successfully",
        "preview_header": "👁️ Data Preview",
        "rows_loaded": "Rows loaded",
        "cols_loaded": "Columns",

        # Header row selection
        "header_row_label": "Header row",
        "header_row_help": "Select the row number containing column headers (default 1)",
        "header_row_preview": "Raw data preview (first 6 rows)",
        "header_row_reload": "Load with selected header row",

        # Aging method
        "method_header": "🔧 Aging Method",
        "method_label": "Select aging method",
        "method_index": "Aging by material index",
        "method_batch": "Aging by material index and batch/lot",

        # Aging date
        "date_header": "📅 Aging Date",
        "date_label": "Select aging calculation date",

        # Column mapping
        "mapping_header": "🗂️ Column Mapping",
        "mapping_desc": "Map file columns to required fields",
        "col_material_index": "Material Index *",
        "col_receipt_date": "Stock Receipt Date *",
        "col_material_name": "Material Name *",
        "col_doc_number": "Receipt Document Number *",
        "col_quantity": "Quantity / Stock Balance *",
        "col_value": "Stock Value (optional)",
        "col_warehouse": "Warehouse (optional)",
        "col_batch": "Batch / Lot Number *",
        "col_select": "-- Select column --",
        "col_skip": "-- Skip --",

        # Aging buckets
        "buckets_header": "📊 Aging Buckets",
        "buckets_type_label": "Bucket type",
        "buckets_default": "Use default aging buckets",
        "buckets_custom": "Define custom aging buckets",
        "buckets_default_title": "Default aging buckets",
        "buckets_custom_title": "Custom aging buckets",
        "bucket_name": "Bucket name",
        "bucket_from": "Day from",
        "bucket_to": "Day to",
        "bucket_to_help": "Leave empty for the final open-ended bucket",
        "bucket_add": "➕ Add bucket",
        "bucket_remove": "Remove",
        "bucket_last_unlimited": "Last bucket is unlimited (no upper bound)",
        "bucket_error_title": "Bucket validation error",
        "bucket_error_overlap": "Aging buckets overlap or are invalid!",
        "bucket_error_order": "Day ranges must be ascending and non-overlapping!",
        "bucket_warn_gap": "Warning: gap detected between buckets",
        "bucket_error_multi_open": "Only the last bucket can have an empty 'Day to'.",
        "bucket_error_empty_name": "Bucket {n}: name is empty.",
        "bucket_error_invalid_from": "Bucket {n}: invalid 'Day from'.",
        "bucket_error_to_lte_from": "Bucket '{name}': 'Day to' must be greater than 'Day from'.",
        "bucket_error_overlaps": "Bucket '{name}': overlaps with previous bucket.",
        "bucket_error_none": "No buckets defined.",
        "bucket_error_only_one_open": "Only one bucket can be open-ended (no 'Day to').",

        # Calculate
        "calc_button": "🔄 Calculate Aging",
        "calc_success": "✅ Aging calculated successfully!",
        "calc_error": "❌ Error during aging calculation",

        # Download
        "download_button": "⬇️ Download Excel Report",
        "download_generating": "Generating Excel file...",

        # Dashboard
        "dashboard_header": "📈 Dashboard",
        "kpi_total_qty": "Total Quantity",
        "kpi_total_value": "Total Value",
        "kpi_materials": "Material Indexes",
        "kpi_warehouses": "Warehouses",
        "kpi_above_1y": "Share above 1 year",
        "kpi_above_2y": "Share above 2 years",
        "chart_qty_title": "Aging by Quantity",
        "chart_val_title": "Aging by Value",
        "chart_wh_title": "Aging by Warehouse",
        "chart_top10_old": "Top 10 Oldest Material Indexes",
        "chart_top10_val": "Top 10 Highest Value Aged Items",
        "chart_qty_axis": "Quantity",
        "chart_val_axis": "Value",
        "chart_bucket_axis": "Aging Bucket",
        "chart_material_axis": "Index / Name",
        "chart_wh_axis": "Warehouse",

        # Results tabs
        "tab_dashboard": "📊 Dashboard",
        "tab_detail": "📋 Detailed Data",
        "tab_qty_summary": "📦 Quantity Summary",
        "tab_val_summary": "💰 Value Summary",
        "tab_wh_summary": "🏭 Warehouse Summary",
        "tab_batch_summary": "🏷️ Batch Summary",
        "tab_validation": "⚠️ Validation",

        # Validation
        "validation_header": "Validation Log",
        "val_row": "Row",
        "val_type": "Issue Type",
        "val_desc": "Description",
        "val_severity": "Severity",
        "val_no_issues": "✅ No validation issues found",
        "val_issues_found": "issues found",
        "severity_error": "ERROR",
        "severity_warning": "WARNING",
        "severity_info": "INFO",

        # Info messages
        "info_no_value_col": "ℹ️ Value column not mapped — value aging skipped.",
        "info_no_wh_col": "ℹ️ Warehouse column not mapped — warehouse summary skipped.",
        "info_batch_required": "⚠️ For batch aging, the batch/lot column is required.",

        # Excel sheet names
        "sheet_detail": "Detailed_Data",
        "sheet_qty": "Aging_Quantity",
        "sheet_val": "Aging_Value",
        "sheet_wh": "Aging_By_Warehouse",
        "sheet_batch": "Aging_By_Batch",
        "sheet_summary": "Summary",
        "sheet_validation": "Validation_Log",

        # Column names in output
        "out_aging_date": "Aging Date",
        "out_age_days": "Age (days)",
        "out_age_months": "Age (months)",
        "out_bucket": "Aging Bucket",
        "out_method": "Aging Method",
        "out_validation": "Validation Status",

        # Default bucket labels
        "bucket_0_3": "0–3 months",
        "bucket_3_6": "3–6 months",
        "bucket_6_9": "6–9 months",
        "bucket_9_12": "9–12 months",
        "bucket_1_2": "1–2 years",
        "bucket_2plus": "Above 2 years",

        # Steps/instructions
        "step1": "Step 1: Load file",
        "step2": "Step 2: Configure analysis",
        "step3": "Step 3: Results",
        "instructions": "Start by uploading an Excel or CSV file with inventory data.",
        "error_missing_cols": "Missing required column mappings: ",
        "error_file_read": "Cannot read file. Check format and try again.",
        "error_date_col": "Date column contains invalid values.",
        "ok": "OK",
        "warning": "Warning",
        "total": "Total",
        "mandatory_cols": "Mandatory columns",
        "optional_cols": "Optional columns",
        "batch_col_required": "Batch column (required)",
    }
}


def get_t(lang: str) -> dict:
    """Return translation dictionary for given language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"])
