#!/usr/bin/env python
import argparse
import json
from pathlib import Path
import requests
from typing import List, Dict

def download_single_image(url: str, output_path: Path) -> None:
    if output_path.exists():
        print(f"Skipped {url} — already exists at {output_path}")
        return

    try:
        print(f"Downloading {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        output_path.write_bytes(response.content)
        print(f"Downloaded {url} to {output_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def download_image_and_instructions(image_url: str, instr_url: str, image_path: Path, instr_path: Path) -> None:
    download_single_image(image_url, image_path)
    download_single_image(instr_url, instr_path)

def download_images(faction: str, year: str, names: List[str], base_dir: Path = Path("downloaded_images")) -> None:
    robots_dir = base_dir / "robots"
    instr_dir = base_dir / "instructions"
    robots_dir.mkdir(parents=True, exist_ok=True)
    instr_dir.mkdir(parents=True, exist_ok=True)

    base_url = "https://supply-your-own-url.lol"

    for name in names:
        image_url = f"{base_url}/{faction}/{year}/{name}.jpg"
        instr_url = f"{base_url}/instructions/{faction}/{year}/instr_{name}.jpg"

        image_path = robots_dir / f"{name}.jpg"
        instr_path = instr_dir / f"{name}.jpg"

        download_image_and_instructions(image_url, instr_url, image_path, instr_path)

def download_faction_years(faction: str, years: List[Dict]) -> None:
    for entry in years:
        year = entry["year"]
        names = entry["names"]
        download_images(faction, year, names)

def download_all_factions(data: List[Dict]) -> None:
    for faction_entry in data:
        faction = faction_entry["faction"]
        years = faction_entry["years"]
        download_faction_years(faction, years)

def load_factions_data(json_path: Path) -> List[Dict]:
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def parse_args():
    parser = argparse.ArgumentParser(description="Download Transformers images and instruction scans.")
    parser.add_argument("-d", "--data", type=Path, default=Path("factions.json"),
                        help="Path to JSON file with faction/year/name data (default: factions.json)")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    if not args.data.exists():
        print(f"Missing data file: {args.data}")
        return

    factions_data = load_factions_data(args.data)
    download_all_factions(factions_data)

if __name__ == "__main__":
    main()
