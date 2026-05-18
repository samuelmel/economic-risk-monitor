from src.extract.world_bank_extractor import WorldBankExtractor


def main():
    extractor = WorldBankExtractor()
    extractor.extract_all()


if __name__ == "__main__":
    main()