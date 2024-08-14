import pandas as pd

from models.certificate import Certificate


class CertificateFactory:
    @staticmethod
    def create_one_certificate(row: pd.Series) -> Certificate:
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
        return [
            CertificateFactory.create_one_certificate(row) for _, row in df.iterrows()
        ]
