from src.extract.world_bank_extractor import WorldBankExtractor
from src.transform.raw_to_silver import RawToSilverTransformer


def main():
    extractor = WorldBankExtractor()
    extractor.extract_all()

    raw_to_silver = RawToSilverTransformer()
    raw_to_silver.run()


if __name__ == "__main__":
    main()