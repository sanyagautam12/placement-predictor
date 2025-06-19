import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}  # Dictionary to store separate encoders for each categorical column
        self.scaler = StandardScaler()
        self.numerical_columns = ['age', 'cgpa', 'projects', 'internships', 'certifications',
                                'communication_skill', 'problem_solving_skill', 'extracurriculars']
        self.categorical_columns = ['gender', 'department']
        self.skill_columns = ['python_skill', 'dsa_skill', 'webdev_skill', 'ml_skill']
        
        # Initialize separate label encoders for each categorical column
        for col in self.categorical_columns:
            self.label_encoders[col] = LabelEncoder()
        
    def preprocess_data(self, data, is_training=False):
        """
        Preprocess the input data for model training or prediction
        
        Args:
            data (pd.DataFrame): Input data
            is_training (bool): Whether preprocessing is for training data
            
        Returns:
            pd.DataFrame: Preprocessed data
        """
        df = data.copy()
        
        # Handle categorical variables
        for col in self.categorical_columns:
            if is_training:
                df[col] = self.label_encoders[col].fit_transform(df[col])
            else:
                df[col] = self.label_encoders[col].transform(df[col])
        
        # Scale numerical features
        if is_training:
            df[self.numerical_columns] = self.scaler.fit_transform(df[self.numerical_columns])
        else:
            df[self.numerical_columns] = self.scaler.transform(df[self.numerical_columns])
        
        # Skills are already binary (0/1)
        
        # Drop name column if exists (not needed for prediction)
        if 'name' in df.columns:
            df = df.drop('name', axis=1)
            
        return df
    
    def get_feature_names(self):
        """
        Get list of feature names in correct order for the model
        
        Returns:
            list: List of feature names
        """
        return (self.numerical_columns + 
                self.categorical_columns + 
                self.skill_columns)

def prepare_single_prediction(data_dict, preprocessor):
    """
    Prepare single student data for prediction
    
    Args:
        data_dict (dict): Dictionary containing student data
        preprocessor (DataPreprocessor): Trained preprocessor object
        
    Returns:
        pd.DataFrame: Preprocessed data ready for prediction
    """
    # Convert single data point to DataFrame
    df = pd.DataFrame([data_dict])
    
    # Preprocess the data
    processed_df = preprocessor.preprocess_data(df, is_training=False)
    
    # Ensure correct feature order
    feature_names = preprocessor.get_feature_names()
    return processed_df[feature_names]