import export_stock_data
import transform_stock_data
import load_stock_data

def etl_start():
    extract_data = export_stock_data.export_data()
    print("Extract Finish")

    transform_data = transform_stock_data.transfom_data(extract_data)
    print("Transform Finish")

    load_stock_data.mongodb_data_to_postgresql(transform_data)
    print("Load Finish")


if __name__ == "__main__":
    etl_start()