import os
import argparse
from trainer import model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Vertex custom container training args. These are set by Vertex AI during training but can also be overwritten.
    parser.add_argument('--model-dir', dest='model-dir',
                        default=os.environ['AIP_MODEL_DIR'], type=str, help='GCS URI for saving model artifacts.')
    
    #parser.add_argument('--url', type=str, required=True, help='URL of the new training data')
    #parser.add_argument('--new-data-path', type=str, required=True, help='Path to the new data for predictions')
    
    args = parser.parse_args()
    hparams = args.__dict__
    
    # Assuming new_data is in CSV format and can be loaded into a DataFrame
    #new_data = pd.read_csv(args.new_data_path)
    
    predictions = model.run_model()
    
