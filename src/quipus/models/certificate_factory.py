import pandas as pd

from .certificate import Certificate


class CertificateFactory:
    """
    Factory class to create Certificate objects
    
    Methods:
        - create_one_certificate: create a single Certificate object from a pd.Series
        - create_certificates: create a list of Certificate objects from a DataFrame
    """
    @staticmethod
    def create_one_certificate(row: pd.Series) -> Certificate:
        """
        Create a single Certificate object from a row in a DataFrame
        
        Args:
            row (pd.Series): a row in a DataFrame containing the certificate data
            
        Returns:
            Certificate: a Certificate object created from the row
        """
        return Certificate(
            completion_date=row["completion_date"],
            content=row["content"],
            entity=row["entity"],
            name=row["name"],
            duration=row.get("duration", None),
            validity_checker=row.get("validity_checker", None),
        )

    @staticmethod
    def create_certificates(df: pd.DataFrame) -> list[Certificate]:
        """
        Create a list of Certificate objects from a DataFrame
        
        Args:
            df (pd.DataFrame): a DataFrame containing the certificate data
            
        Returns:
            list[Certificate]: a list of Certificate objects created from the DataFrame
        """
        return [
            CertificateFactory.create_one_certificate(row) for _, row in df.iterrows()
        ]
