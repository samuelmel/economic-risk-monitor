from src.extract.world_bank_extractor import WorldBankExtractor
from src.transform.raw_to_silver import RawToSilverTransformer
from src.transform.silver_to_gold import SilverToGoldTransformer


def main():
    extractor = WorldBankExtractor()
    extractor.extract_all()

    raw_to_silver = RawToSilverTransformer()
    raw_to_silver.run()

    silver_to_gold = SilverToGoldTransformer()
    silver_to_gold.run()


if __name__ == "__main__":
    main()