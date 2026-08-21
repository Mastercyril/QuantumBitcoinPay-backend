"""View Quantum Pay ecosystem statistics"""
import sqlite3
from pathlib import Path

def view_stats():
    db_path = Path("quantumpay.db")
    
    if not db_path.exists():
        print("❌ Database not found. Run the daily executor first.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("╔══════════════════════════════════════════════════╗")
    print("║     QUANTUM PAY ECOSYSTEM - STATISTICS          ║")
    print("╚══════════════════════════════════════════════════╝\n")
    
    # Wallet stats
    cursor.execute('SELECT COUNT(*) FROM wallets')
    total_wallets = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(qsam_balance), SUM(total_rewards) FROM wallets')
    result = cursor.fetchone()
    total_qsam = result[0] or 0
    total_rewards = result[1] or 0
    
    print(f"💰 WALLETS")
    print(f"   Total Wallets:        {total_wallets}")
    print(f"   Total QSAM:           {total_qsam:.2f}")
    print(f"   Total Rewards Paid:   {total_rewards:.2f}")
    print()
    
    # Transaction stats
    cursor.execute('SELECT COUNT(*) FROM transactions')
    total_txs = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM transactions WHERE status="COMPLETED"')
    completed_txs = cursor.fetchone()[0]
    
    print(f"🔗 TRANSACTIONS")
    print(f"   Total Transactions:   {total_txs}")
    print(f"   Completed:            {completed_txs}")
    print()
    
    # Download stats
    cursor.execute('SELECT COUNT(*) FROM downloads')
    total_downloads = cursor.fetchone()[0]
    
    print(f"📥 DOWNLOADS")
    print(f"   Total Downloads:      {total_downloads}")
    print()
    
    # Daily runs
    cursor.execute('SELECT COUNT(*) FROM daily_runs')
    total_runs = cursor.fetchone()[0]
    
    cursor.execute('SELECT run_date, status FROM daily_runs ORDER BY run_id DESC LIMIT 5')
    recent_runs = cursor.fetchall()
    
    print(f"📊 DAILY RUNS")
    print(f"   Total Runs:           {total_runs}")
    if recent_runs:
        print(f"   Recent Runs:")
        for run_date, status in recent_runs:
            print(f"     • {run_date}: {status}")
    print()
    
    # Top wallets
    cursor.execute('SELECT unique_code, qsam_balance FROM wallets ORDER BY qsam_balance DESC LIMIT 5')
    top_wallets = cursor.fetchall()
    
    if top_wallets:
        print(f"🏆 TOP WALLETS BY BALANCE")
        for i, (code, balance) in enumerate(top_wallets, 1):
            print(f"   {i}. {code}: {balance:.2f} QSAM")
    
    conn.close()
    print("\n═══════════════════════════════════════════════════")

if __name__ == "__main__":
    view_stats()
