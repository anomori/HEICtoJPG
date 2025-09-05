import argparse
import concurrent.futures as futures
import os
from pathlib import Path

from PIL import Image
import pillow_heif
from tqdm import tqdm


def convert_one(src_path: Path, dst_dir: Path, to_png: bool, quality: int):
    try:
        heif = pillow_heif.read_heif(str(src_path))
        img = Image.frombytes(heif.mode, heif.size, heif.data, "raw")
        # EXIFをできるだけ引き継ぐ
        exif = heif.metadata.get("exif") if hasattr(heif, "metadata") else None

        if to_png:
            out_path = dst_dir / (src_path.stem + ".png")
            img.save(out_path, format="PNG")  # PNGは可逆
        else:
            out_path = dst_dir / (src_path.stem + ".jpg")
            save_kwargs = {"format": "JPEG", "quality": quality, "optimize": True}
            if exif:
                save_kwargs["exif"] = exif
            img = img.convert("RGB")  # JPEGはRGB前提
            img.save(out_path, **save_kwargs)
        return (src_path, None)
    except Exception as e:
        return (src_path, e)


def main():
    parser = argparse.ArgumentParser(description="Convert HEIC to JPEG/PNG (batch).")
    parser.add_argument("--src", required=True, help="HEICが入ったフォルダ")
    parser.add_argument("--dst", required=True, help="出力フォルダ（なければ作成）")
    parser.add_argument("--png", action="store_true", help="PNGで保存（可逆）")
    parser.add_argument("--quality", type=int, default=95, help="JPEG品質(1-100)")
    parser.add_argument(
        "--workers", type=int, default=os.cpu_count() or 4, help="並列数"
    )
    args = parser.parse_args()

    src_dir = Path(args.src)
    dst_dir = Path(args.dst)
    dst_dir.mkdir(parents=True, exist_ok=True)

    # サブフォルダも含めて拾う場合は rglob に変更
    heics = list(src_dir.glob("*.heic")) + list(src_dir.glob("*.HEIC"))
    if not heics:
        print("HEICファイルが見つかりませんでした。--src のパスを確認してください。")
        return

    print(f"変換対象: {len(heics)} 枚 / 出力: {dst_dir}")
    to_png = args.png
    quality = args.quality

    results = []
    with futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for res in tqdm(
            ex.map(lambda p: convert_one(p, dst_dir, to_png, quality), heics),
            total=len(heics),
        ):
            results.append(res)

    # 失敗報告
    fails = [r for r in results if r[1] is not None]
    if fails:
        print(f"\n失敗: {len(fails)} 件")
        for p, e in fails[:10]:
            print(f"- {p.name}: {e}")
        if len(fails) > 10:
            print("...他省略")
    else:
        print("\nすべて成功しました。")


if __name__ == "__main__":
    # HEIFプラグインの有効化（pillow-heif）
    pillow_heif.register_heif_opener()
    main()
