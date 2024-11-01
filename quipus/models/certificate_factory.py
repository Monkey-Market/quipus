from typing import TypeAlias, Union, Iterator, Tuple, Any, Dict, List

import polars as pl

from .certificate import Certificate


PolarsRow: TypeAlias = Union[Iterator[Tuple[Any, ...]], Iterator[Dict[str, Any]]]


class CertificateFactory:
    """
    Factory class to create Certificate objects
    
    Methods:
        - create_one_certificate: create a single Certificate object from a pd.Series
        - create_certificates: create a list of Certificate objects from a DataFrame
    """
    @staticmethod
    def create_one_certificate(row: PolarsRow) -> Certificate:
        """
        Create a single Certificate object from a row in a DataFrame
        
        Args:
            row (PolarsRow): a row in a DataFrame containing the certificate data
            
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
    def create_certificates(df: pl.DataFrame) -> List[Certificate]:
        """
        Create a list of Certificate objects from a DataFrame
        
        Args:
            df (pl.DataFrame): a DataFrame containing the certificate data
            
        Returns:
            List[Certificate]: a list of Certificate objects created from the DataFrame
        """
        return [
            CertificateFactory.create_one_certificate(row)
            for row in df.iter_rows(named=True)
        ]
