
import argparse
import os
import warnings
from datetime import datetime, timedelta 


today_date = datetime.today()

this_year = today_date.isoformat().split('-')[0]
print(this_year)

# adapted from GEMwiki/launcher.py

# Filter DeprecationWarning or FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)


def main():
    # make necessary directories if they don't exist
    # INSERT directory making things here from all_config.py and TODO tabs
    # list of trackers currently supported
    # trackers = ["cement", "coal mine", "combustion", "GOGET", "geothermal", "hydro", "iron mine", "methane", "nuclear", "solar", "steel", "wind"]
    list_of_all_official = ["Oil & Gas Plants", "Coal Plants", "Solar", "Wind", "Nuclear", "Hydropower", "Bioenergy", "Geothermal", "Coal Terminals", "Oil & Gas Extraction", "Coal Mines", "LNG Terminals", "Gas Pipelines", "Oil Pipelines", "Iron & Steel", "Iron ore Mines", "Cement and Concrete"]
    tracker_mapnames = ["europe", "africa", "integrated", "asia", "latam", "ggit", "goit", "goget", "gctt", "gcpt", "gcmt", "gogpt", "gspt", "gwpt", "gnpt", "gbpt", "ggpt", "ghpt", "gist", "gmet", "giomt"]

    month_number = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    } 
    
    
    # create arg parser and argument details
    parser = argparse.ArgumentParser(description="Dispatcher for running map file generation and final data s3 upload scripts")
    parser.add_argument("mode", choices=["generate"], help="(req) What mode to run")
    parser.add_argument("project_name", choices=list_of_all_official, help="(req) Name of the project to run")
    parser.add_argument("--releaseiso", choices=[f"{i:02}" for i in range(1, 13)], help="(req) Month of official release")
    parser.add_argument("--priority", choices=tracker_mapnames, help="[generate param] Optionally provide a map file to prioritize")
    parser.add_argument("--new_h2_data", choices=[True, False], help="[generate param] Defaults to being false. Only relevant for maps containing European Gas and Oil Plant data")
    parser.add_argument("--pm_preview_mode", choices=[True, False], help="[generate param] Defaults to being false. Only relevant for GGIT test map Baird uses.")
    parser.add_argument("--simplified", choices=[True, False], help="[generate param] Defaults to being false. Reduces the columns to bare minimum for quickest map rendering.")

    
    
    # parser.add_argument("--output-dir", help="[generate param] Path to the output directory")
    # could pull out upload function to only optionally save to s3

    parser.add_argument("--save-s3", help="[generate param] Uploads all files to digital ocean publicgemdata bucket")
    
    parser.add_argument("--section", choices=["coal emissions", "gas finance", "plumes detected", "ownership tree"], help="[generate_insert param (req)] Which section to generate")

    args = parser.parse_args()

    if args.mode == "generate":
        if args.get_archived_urls:
            import get_archived_urls  # not best practice, but keeps this script less bloated when executing
            get_archived_urls.main()

        if args.get_project_id_name_list:
            import get_project_id_name_list  # not best practice, but keeps this script less bloated when executing
            get_project_id_name_list.main()

        if args.project_name == "steel" and (not args.input_files_steel or len(args.input_files_steel) != 5):
            parser.error("--input-files-steel are required when generating steel, in order: all_fields, iron_yearly_prod, steel_yearly_prod, relining, green_steel")
        elif args.project_name == "coal mine" and (not args.input_files_coal_mine or len(args.input_files_coal_mine) != 2):
            parser.error("--input-files-coal-mine are required when generating coal mine, in order: GCMT main (xlsx), historical production data (xlsx)")
        elif args.project_name not in ["steel", "coal mine"] and not args.input_file:
            parser.error("--input-file is required when generating")

        import MainTrackers  # not best practice, but keeps this script less bloated when executing
        if args.project_name == "cement":
            MainTrackers.generate_cement_wiki(args.input_file, args.output_dir)
        elif args.project_name == "coal mine":
            MainTrackers.generate_coal_mine_wiki(args.input_files_coal_mine, args.output_dir, args.only_production_data)
        elif args.project_name == "combustion":
            MainTrackers.generate_combustion_wiki(args.input_file, args.output_dir)
        elif args.project_name == "GOGET":
            MainTrackers.generate_goget_wiki(args.input_file, args.output_dir)
        elif args.project_name == "geothermal":
            MainTrackers.generate_geothermal_wiki(args.input_file, args.output_dir)
        elif args.project_name == "hydro":
            MainTrackers.generate_hydro_wiki(args.input_file, args.output_dir)
        elif args.project_name == "iron mine":
            MainTrackers.generate_iron_mine_wiki(args.input_file, args.output_dir)
        elif args.project_name == "methane":
            MainTrackers.generate_methane_wiki(args.input_file, args.output_dir)
        elif args.project_name == "nuclear":
            MainTrackers.generate_nuclear_wiki(args.input_file, args.output_dir)
        elif args.project_name == "solar":
            if not os.path.exists("project_id_name_list.csv"):
                parser.error("project_id_name_list.csv must be present when generating solar pages. Try running again with flag '--get-project-id-name-list' to obtain the csv")
            MainTrackers.generate_solar_wiki(args.input_file, args.output_dir)
        elif args.project_name == "steel":
            MainTrackers.generate_steel_wiki(args.input_files_steel, args.output_dir)
        elif args.project_name == "wind":
            if not os.path.exists("project_id_name_list.csv"):
                parser.error("project_id_name_list.csv must be present when generating wind pages. Try running again with flag '--get-project-id-name-list' to obtain the csv")
            MainTrackers.generate_wind_wiki(args.input_file, args.output_dir)

    elif args.mode == "upload":
        if not args.wikisource_directory:
            parser.error("--wikisource-directory is required when uploading")

        import upload_all_wiki  # not best practice, but keeps this script less bloated when executing
        if not args.upload_message:
            upload_all_wiki.main(args.project_name, args.wikisource_directory)
        else:
            upload_all_wiki.main(args.project_name, args.wikisource_directory, args.upload_message)

    elif args.mode == "test_upload":
        if not args.wikisource_directory:
            parser.error("--wikisource-directory is required when testing upload")
        import test_upload_integrity
        test_upload_integrity.main(args.wikisource_directory)

    elif args.mode == "generate_insert":
        if args.get_archived_urls:
            import get_archived_urls  # not best practice, but keeps this script less bloated when executing
            get_archived_urls.main()

        if args.get_project_id_wikiUrl_list:
            import get_project_id_name_list  # not best practice, but keeps this script less bloated when executing
            get_project_id_name_list.main(second_column="wikiUrl")

        if not args.input_file:
            parser.error("--input-file is required when generating")

        import SectionInserts  # not best practice, but keeps this script less bloated when executing
        if args.section == "coal emissions":
            if not os.path.exists("project_id_wikiUrl_list.csv"):
                parser.error("project_id_wikiUrl_list.csv must be present when generating coal emissions sections. Try running again with flag '--get-project-id-wikiUrl-list' to obtain the csv")
            SectionInserts.generate_emissions_data_section(args.input_file)
        elif args.section == "gas finance":
            SectionInserts.generate_gas_finance_section(args.input_file)
        elif args.section == "plumes detected":
            SectionInserts.generate_plumes_detected_section(args.input_file)
        elif args.section == "ownership tree":
            if not os.path.exists("project_id_wikiUrl_list.csv"):
                parser.error("project_id_wikiUrl_list.csv must be present when generating ownership tree sections. Try running again with flag '--get-project-id-wikiUrl-list' to obtain the csv")
            SectionInserts.generate_ownership_tree_section(args.input_file, args.project_name)


if __name__ == "__main__":
    main()
