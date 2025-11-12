"""Quick test av Basic Plan Generator"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.planning.basic_plan_generator import BasicPlanGenerator

db_path = Path(__file__).parent / "data" / "output" / "linkops_history.db"

print(f"DB finns: {db_path.exists()}")
print(f"DB sökväg: {db_path}")

if db_path.exists():
    print("\n🎯 Skapar generator...")
    generator = BasicPlanGenerator(str(db_path))

    print("✅ Generator skapad!")

    planning_data = {117: 15}

    print("\n📊 Genererar plan...")
    try:
        plan = generator.generate_plan(
            planning_data=planning_data,
            plan_name="Quick Test Plan"
        )

        print(f"\n✅ Plan genererad med {plan.total_links} länkar!")

        generator.print_plan_summary(plan)

        output = Path(__file__).parent / "data" / "output" / "quick_test_plan.csv"
        generator.export_to_csv(plan, str(output))

        print(f"\n✅ KLART! Plan exporterad till {output}")

    except Exception as e:
        print(f"\n❌ Fel: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ Databas saknas!")

