#!/usr/bin/env python3
"""
Comprehensive Parliament 45 Re-linking with Higher Standards

This script runs the complete process:
1. Comprehensive cleanup of ALL Parliament 45 evidence links
2. Re-linking with higher quality standards using source-specific thresholds
"""

import logging
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

# Add pipeline directory to path
pipeline_dir = Path(__file__).parent / "pipeline"
sys.path.insert(0, str(pipeline_dir))

from stages.linking.evidence_linker import EvidenceLinker
from stages.linking.progress_scorer import ProgressScorer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

def run_comprehensive_cleanup():
    """Run the comprehensive cleanup process"""
    print("🧹 STEP 1: COMPREHENSIVE CLEANUP")
    print("=" * 50)
    
    # Import and run cleanup
    sys.path.append(str(Path(__file__).parent))
    from comprehensive_parliament_45_cleanup import ComprehensiveParliament45CleanupJob
    
    cleanup_job = ComprehensiveParliament45CleanupJob()
    result = cleanup_job.execute()
    
    if result.status.value == 'success':
        print(f"✅ Cleanup successful!")
        if result.metadata:
            metadata = result.metadata
            print(f"   - Parliament 45 evidence items: {metadata.get('parliament_45_evidence_items', 0)}")
            print(f"   - Promises cleaned: {metadata.get('promises_cleaned', 0)}")
            print(f"   - Evidence items reset: {metadata.get('evidence_items_reset', 0)}")
        return True
    else:
        print(f"❌ Cleanup failed: {result.error_message}")
        return False

def run_high_quality_linking():
    """Run evidence linking with higher quality standards"""
    print("\n🔗 STEP 2: HIGH-QUALITY EVIDENCE LINKING")
    print("=" * 50)
    
    # Configuration with higher standards
    config = {
        'batch_size': 10,
        'max_items_per_run': 1000,  # Process all Parliament 45 evidence
        'semantic_threshold': 0.55,  # Higher base threshold
        'llm_validation_threshold': 0.7,  # Much higher LLM threshold
        'high_similarity_bypass_threshold': 0.65,  # Higher bypass threshold
        'max_llm_candidates': 3,  # Fewer candidates for quality
        'default_parliament_session': '45',
        
        # Source-specific thresholds for quality control
        'source_type_thresholds': {
            'Bill Event (LEGISinfo)': {
                'semantic_threshold': 0.50,  # Bills get reasonable threshold
                'llm_threshold': 0.6,         # Still high quality
                'bypass_threshold': 0.60
            },
            'News Article': {
                'semantic_threshold': 0.60,  # Higher standard for news
                'llm_threshold': 0.75,       # Very high certainty
                'bypass_threshold': 0.70
            },
            'Order in Council': {
                'semantic_threshold': 0.58,  # High standard
                'llm_threshold': 0.72,       # High certainty
                'bypass_threshold': 0.68
            },
            'Canada Gazette': {
                'semantic_threshold': 0.58,  # High standard
                'llm_threshold': 0.72,       # High certainty
                'bypass_threshold': 0.68
            }
        }
    }
    
    print("📊 QUALITY STANDARDS:")
    print(f"   - Base Semantic Threshold: {config['semantic_threshold']}")
    print(f"   - Base LLM Threshold: {config['llm_validation_threshold']}")
    print(f"   - Base Bypass Threshold: {config['high_similarity_bypass_threshold']}")
    print()
    print("📋 SOURCE-SPECIFIC THRESHOLDS:")
    for source_type, thresholds in config['source_type_thresholds'].items():
        print(f"   - {source_type}:")
        print(f"     • Semantic: {thresholds['semantic_threshold']}")
        print(f"     • LLM: {thresholds['llm_threshold']}")
        print(f"     • Bypass: {thresholds['bypass_threshold']}")
    print()
    
    # Create and run the evidence linker
    linker = EvidenceLinker("parliament_45_high_quality_linking", config)
    
    print("🚀 Starting high-quality evidence linking...")
    start_time = time.time()
    
    result = linker.execute(
        limit=1000,
        parliament_session_id='45'
    )
    
    duration = time.time() - start_time
    
    print(f"\n✅ HIGH-QUALITY LINKING COMPLETED")
    print("=" * 40)
    print(f"📊 Status: {result.status.value}")
    print(f"⏰ Duration: {duration:.2f} seconds")
    print(f"📈 Items Processed: {result.items_processed}")
    print(f"📈 Items Updated: {result.items_updated}")
    print(f"📈 Items Skipped: {result.items_skipped}")
    print(f"❌ Errors: {result.errors}")
    
    if result.metadata:
        optimizations = result.metadata.get('optimizations', {})
        print(f"\n🚀 Optimizations Used:")
        print(f"   - Bill Linking Bypasses: {optimizations.get('bill_linking_bypasses', 0)}")
        print(f"   - High Similarity Bypasses: {optimizations.get('high_similarity_bypasses', 0)}")
        print(f"   - Batch LLM Validations: {optimizations.get('batch_llm_validations', 0)}")
        
        affected_promises = result.metadata.get('affected_promise_ids', set())
        print(f"   - Promises Affected: {len(affected_promises)}")
    
    return result.status.value == 'success', result

def main():
    """Main execution function"""
    print("🎯 COMPREHENSIVE PARLIAMENT 45 RE-LINKING")
    print("🎯 WITH HIGHER QUALITY STANDARDS")
    print("=" * 60)
    print("This process will:")
    print("1. Remove ALL existing Parliament 45 evidence links")
    print("2. Reset ALL Parliament 45 evidence items to pending")
    print("3. Re-link with much higher quality thresholds")
    print("4. Use source-specific standards to reduce false positives")
    print()
    
    # Step 1: Comprehensive cleanup
    cleanup_success = run_comprehensive_cleanup()
    if not cleanup_success:
        print("❌ Cleanup failed, aborting re-linking process")
        return False
    
    # Wait a moment for database consistency
    print("\n⏳ Waiting 5 seconds for database consistency...")
    time.sleep(5)
    
    # Step 2: High-quality linking
    linking_success = run_high_quality_linking()
    
    if linking_success:
        print("\n🎉 COMPREHENSIVE RE-LINKING SUCCESSFUL!")
        print("✨ Parliament 45 evidence now linked with higher quality standards")
        print("✨ Timeline should show fewer false positives")
        return True
    else:
        print("\n⚠️  Re-linking completed with issues")
        return False

if __name__ == "__main__":
    try:
        success = main()
        exit_code = 0 if success else 1
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logging.error("Comprehensive re-linking failed", exc_info=True)
        sys.exit(1) 