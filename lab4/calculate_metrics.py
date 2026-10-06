"""Лаб 4-ийн симуляцын хугацаа, WIP-г тооцно. Нэмэлт сан шаардлагагүй."""
import csv
from pathlib import Path
from statistics import mean


def main():
    with Path(__file__).with_name("flow-data.csv").open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    if not rows or len({r["id"] for r in rows}) != len(rows):
        raise ValueError("Картын ID хоосон эсвэл давхардсан байна")
    for r in rows:
        for field in ("created", "started", "review", "done"):
            r[field] = int(r[field])
        if not 0 <= r["created"] <= r["started"] <= r["review"] <= r["done"]:
            raise ValueError(f"Хугацааны дараалал буруу: {r['id']}")
    print("ID     Lead  Cycle  Waiting (өдөр)")
    for r in rows:
        print(f"{r['id']}  {r['done']-r['created']:4}  {r['done']-r['started']:5}  {r['started']-r['created']:7}")
    for label, start, end in (("Lead", "created", "done"), ("Cycle", "started", "done"), ("Waiting", "created", "started")):
        print(f"Дундаж {label}: {mean(r[end]-r[start] for r in rows):.2f} өдөр")
    first, last = min(r["created"] for r in rows), max(r["done"] for r in rows)
    duration = last - first
    print(f"Throughput: {len(rows) / duration:.2f} story/өдөр" if duration else "Throughput: хугацааны интервал 0")
    print("Өдөр  To Do  In Progress  Review  Done")
    max_active = max_review = 0
    for day in range(first, last + 1):
        todo = sum(r["created"] <= day < r["started"] for r in rows)
        active = sum(r["started"] <= day < r["review"] for r in rows)
        review = sum(r["review"] <= day < r["done"] for r in rows)
        done = sum(r["done"] <= day for r in rows)
        max_active, max_review = max(max_active, active), max(max_review, review)
        if active > 3 or review > 2:
            raise ValueError(f"D{day}: WIP хязгаар зөрчсөн")
        print(f"D{day:<3}  {todo:5}  {active:11}  {review:6}  {done:4}")
    print(f"WIP шалгалт: PASS (In Progress {max_active}/3, Review {max_review}/2)")


if __name__ == "__main__":
    main()
