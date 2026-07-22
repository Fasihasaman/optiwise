from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import services.model_store as model_store
import pandas as pd
import numpy as np
import traceback


def train_model(df):

    try:

        df = df.copy()

        
        # REMOVE NULL VALUES
        

        df = df.dropna()

        if len(df) < 10:

            print("MODEL ERROR: Not enough rows")

            return None

        
        # HANDLE DATE COLUMNS
        

        for col in df.columns:

            try:

                if "date" in col.lower():

                    df[col] = pd.to_datetime(
                        df[col],
                        errors="coerce"
                    )

                    df[col] = (
                        df[col]
                        .astype("int64")
                        // 10**9
                    )

            except:
                pass

        
        # ENCODE TEXT COLUMNS
        

        for col in df.select_dtypes(
            include=["object"]
        ).columns:

            try:

                encoder = LabelEncoder()

                df[col] = encoder.fit_transform(
                    df[col].astype(str)
                )

            except Exception as e:

                print(
                    f"Encoding Error in {col}:",
                    e
                )

        
        # KEEP NUMERIC DATA ONLY
        

        df = df.select_dtypes(
            include=[np.number]
        )

        
        # CHECK DATA
        

        if df.shape[1] < 2:

            print(
                "MODEL ERROR: Need at least 2 numeric columns"
            )

            return None

        if len(df) > 5000:
           df = df.sample(5000, random_state=42)
        # FEATURES & TARGET
        

        X = df.iloc[:, :-1]

        y = df.iloc[:, -1]

        
        # REMOVE INF VALUES
        

        X = X.replace(
            [np.inf, -np.inf],
            np.nan
        )

        X = X.fillna(0)

        y = y.replace(
            [np.inf, -np.inf],
            np.nan
        )

        y = y.fillna(0)

       
        # TRAIN MODEL
       

        model = RandomForestRegressor(
        n_estimators=10,
        random_state=42,
        n_jobs=1
        )
        model.fit(X, y)
        model_store.model = model
        model_store.X_columns = list(X.columns)
        model_store.target_column = y.name
        predictions = model.predict(
            X.head(5)
        )

        print(
            "MODEL TRAINED SUCCESSFULLY"
        )

        return {

            "model": model,

            "X": X,

            "y": y,

            "predictions": predictions.tolist()

        }

    except Exception as e:

        print("\n MODEL ERROR ")

        traceback.print_exc()

        print("Error:", str(e))

        print("\n")

        return None