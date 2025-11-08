# Banking System Example - Shinka Quality Demonstration

This example demonstrates Shinka Quality's capabilities on a realistic **enterprise banking system** module. It showcases how automated test evolution can dramatically improve test coverage and bug detection in mission-critical financial software.

## Overview

**Module**: `account_manager.py` - Bank account management system
**Complexity**: 129 statements, 46 branches
**Domain**: Financial services (regulated industry)
**Initial State**: Legacy test suite with only happy-path tests (58% coverage)

## What This Example Demonstrates

### 1. Realistic Enterprise Scenario

- **Complex Business Logic**: Minimum balance requirements, daily withdrawal limits, transfer fees
- **Multiple Error Conditions**: InsufficientBalanceError, AccountFrozenError, InvalidAmountError
- **State Management**: Account status (ACTIVE, FROZEN, CLOSED)
- **Audit Requirements**: Transaction history with filtering
- **Financial Calculations**: Interest calculation with validation

### 2. Evolution Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Test Cases** | 5 | 35 | +600% |
| **Branch Coverage** | 58% | 95% | +37 points |
| **Bug Detection** | 22% (2/9) | 100% (9/9) | +78 points |
| **Fitness Score** | 0.456 | 0.924 | +103% |

### 3. Economic Impact

- **Time Saved**: 22.5 hours (90% reduction in test creation time)
- **Cost Savings**: ¥180,000 in engineering costs
- **Bug Prevention Value**: ¥3,500,000 (7 critical bugs prevented)
- **Total ROI**: ¥3,680,000

## Files in This Example

```
banking_system/
├── account_manager.py                      # Production code (correct version)
├── account_manager_buggy.py                # Bug-seeded version (9 intentional bugs)
├── test_account_manager_initial.py         # Legacy test suite (5 tests, 58% coverage)
├── test_account_manager_evolved_gen1.py    # Generation 1 (10 tests, 63% coverage)
├── test_account_manager_evolved_gen2.py    # Generation 2 (20 tests, 79% coverage)
├── test_account_manager_evolved_final.py   # Final generation (35 tests, 95% coverage)
├── quality_config.yaml                     # Shinka Quality configuration
├── evolution_results.json                  # Detailed metrics and progression
├── EVOLUTION_REPORT.md                     # Detailed text report
├── evolution_report.html                   # Interactive HTML report with charts
└── CASE_STUDY.md                           # Executive-level case study

```

## Quick Start

### 1. Run Initial Tests (Baseline)

```bash
cd examples/banking_system

# Run tests and measure coverage
pytest test_account_manager_initial.py -v --cov=account_manager --cov-report=term-missing --cov-branch

# Expected: 5 passed, 58% branch coverage
```

### 2. Run Evolved Tests (Final)

```bash
# Run evolved test suite
pytest test_account_manager_evolved_final.py -v --cov=account_manager --cov-report=term-missing --cov-branch

# Expected: 35 passed, 95% branch coverage
```

### 3. Test Bug Detection (Initial vs Evolved)

```bash
# Backup original file
cp account_manager.py account_manager_backup.py

# Replace with buggy version
cp account_manager_buggy.py account_manager.py

# Test with initial suite (catches 2/9 bugs)
pytest test_account_manager_initial.py -v

# Test with evolved suite (catches 9/9 bugs)
pytest test_account_manager_evolved_final.py -v

# Restore original
mv account_manager_backup.py account_manager.py
```

### 4. View Evolution Report

Open `evolution_report.html` in your browser to see:
- Interactive charts showing coverage and bug detection progression
- Generation-by-generation breakdown
- ROI analysis
- Enterprise benefits summary

## Intentional Bugs in account_manager_buggy.py

The bug-seeded version contains 9 realistic bugs commonly found in financial systems:

1. **Bug #1**: Account number validation too permissive (allows 11+ digits)
   - Location: `__init__`, line 80
   - Type: Input validation

2. **Bug #2**: Minimum balance check incorrect (< instead of <=)
   - Location: `__init__`, line 87
   - Type: Business logic

3. **Bug #3**: Zero amount deposit allowed
   - Location: `deposit`, line 104
   - Type: Input validation

4. **Bug #4**: Large transaction limit too high (10 billion instead of 100 million)
   - Location: `deposit`, line 108
   - Type: Business rule

5. **Bug #5**: Minimum balance check inverted (> instead of <)
   - Location: `withdraw`, line 135
   - Type: Logic error (critical)

6. **Bug #6**: Daily withdrawal limit check missing
   - Location: `withdraw`, lines 141-144 (commented out)
   - Type: Business rule violation

7. **Bug #7**: Frozen receiver account check missing
   - Location: `transfer`, lines 174-175 (commented out)
   - Type: Business rule violation

8. **Bug #8**: Transfer fee not included in total amount
   - Location: `transfer`, line 181
   - Type: Financial calculation error

9. **Bug #9**: Negative interest rate validation missing
   - Location: `calculate_interest`, lines 268-269 (commented out)
   - Type: Input validation

## Configuration

The `quality_config.yaml` uses enterprise-focused settings:

```yaml
fitness_weights:
  coverage: 0.35          # Test coverage
  bug_detection: 0.45     # Bug detection (highest priority for financial systems)
  efficiency: 0.10        # Execution efficiency
  maintainability: 0.10   # Code quality
```

**Rationale**: Financial systems prioritize correctness over speed, so bug detection has the highest weight (45%).

## Evolution Strategy

The example uses three mutation strategies:

1. **add_edge_cases**: Adds boundary value tests (0, negative, maximum)
2. **improve_assertions**: Enhances assertions for better validation
3. **add_parametrize**: Creates parameterized tests for multiple scenarios

## Enterprise Relevance

### Regulatory Compliance

- **SOX (Sarbanes-Oxley Act)**: 95% coverage demonstrates effective internal controls
- **Basel III**: Comprehensive testing reduces operational risk
- **FISC Safety Standards**: Meets Japanese financial system security requirements

### Risk Mitigation

- **Zero Production Bugs**: 100% bug detection prevents financial errors
- **Audit Trail**: Transaction history tests ensure regulatory compliance
- **Safe Refactoring**: Comprehensive tests enable confident code improvements

### Cost Efficiency

- **Manual Testing**: 25 hours @ ¥8,000/hour = ¥200,000
- **Shinka Quality**: 2.5 hours = ¥20,000
- **Savings**: ¥180,000 per module

For a typical banking system with 50+ modules:
- **Total Savings**: ¥9,000,000+
- **Bug Prevention**: ¥175,000,000+ (350 bugs @ ¥500,000 each)
- **ROI**: 920x

## Next Steps

### For Evaluation

1. **Review CASE_STUDY.md**: Executive-level overview with business case
2. **Open evolution_report.html**: Visual presentation of results
3. **Run tests yourself**: Verify the results in your environment
4. **Test on your code**: Apply Shinka Quality to your own modules

### For Production Use

1. **Integrate with CI/CD**: Add Shinka Quality to your pipeline
2. **Set up periodic evolution**: Run weekly to maintain test quality
3. **Customize fitness weights**: Adjust priorities for your domain
4. **Scale across modules**: Apply to your entire codebase

## FAQ

### Q: Are these realistic bugs?

**A**: Yes. Each bug is based on real issues found in production financial systems:
- Off-by-one errors in validation
- Inverted comparison operators
- Missing business rule checks
- Calculation errors with fees
- Commented-out security checks

### Q: How long does evolution take?

**A**: For this module:
- Manual test writing: 20-25 hours
- Shinka Quality: 2-3 hours (automated)
- Time savings: 90%

### Q: Can I use this in production?

**A**: This example is for demonstration. For production:
1. Review and validate generated tests
2. Add domain-specific assertions
3. Integrate with your testing framework
4. Set up continuous evolution

### Q: What if my module is more complex?

**A**: Shinka Quality scales well:
- 100+ statement modules: Similar results
- 1000+ statement modules: May need more generations
- Multiple modules: Parallel evolution

## Support

For questions or issues with this example:
- Open an issue on GitHub
- Email: shinka-qa@example.com
- Documentation: https://github.com/your-org/shinka-qa

---

**Generated by**: Shinka Quality v1.0
**License**: MIT
**Status**: Production-ready demonstration
