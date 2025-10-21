"""
Evaluator functions for Clinical Genomics Decision Support domain.
"""

from lbx_cli.mcpuniverse.evaluator.functions import compare_func
import json
import re


@compare_func
def validate_variant_classification(llm_response, question: str, expected_tier: str, 
                                     expected_codes: list, min_confidence: float = 0.8,
                                     must_have_reference: bool = True):
    """
    Validates ACMG/AMP variant classification response.
    
    Checks:
    - Correct pathogenicity tier
    - Presence of expected ACMG evidence codes
    - Confidence score meets threshold
    - Clinical recommendation is present
    - References are provided
    """
    try:
        # Extract the agent's response
        result = llm_response.result if hasattr(llm_response, 'result') else llm_response
        
        # Parse JSON if string
        if isinstance(result, str):
            data = json.loads(result)
        else:
            data = result
        
        issues = []
        score = 0
        max_score = 5
        
        # 1. Check pathogenicity tier (20%)
        pathogenicity = data.get('pathogenicity', '').lower()
        expected_lower = expected_tier.lower()
        
        if expected_lower in pathogenicity or pathogenicity in expected_lower:
            score += 1
        else:
            issues.append(f"Pathogenicity: expected '{expected_tier}', got '{data.get('pathogenicity')}'")
        
        # 2. Check evidence codes (30%)
        evidence_codes = data.get('evidence_codes', [])
        if not isinstance(evidence_codes, list):
            evidence_codes = []
        
        # Check if at least 60% of expected codes are present
        matched_codes = sum(1 for code in expected_codes if any(code in str(ec) for ec in evidence_codes))
        if matched_codes >= len(expected_codes) * 0.6:
            score += 1.5
        else:
            issues.append(f"Evidence codes: expected {expected_codes}, got {evidence_codes} (only {matched_codes}/{len(expected_codes)} matched)")
        
        # 3. Check confidence score (20%)
        confidence = data.get('confidence', 0)
        try:
            confidence_val = float(confidence)
            if confidence_val >= min_confidence:
                score += 1
            else:
                issues.append(f"Confidence too low: {confidence_val} < {min_confidence}")
        except (ValueError, TypeError):
            issues.append(f"Invalid confidence value: {confidence}")
        
        # 4. Check clinical recommendation (15%)
        clinical_rec = data.get('clinical_recommendation', '')
        if clinical_rec and len(str(clinical_rec).strip()) > 20:
            score += 0.75
        else:
            issues.append("Clinical recommendation missing or too brief")
        
        # 5. Check references (15%)
        references = data.get('references', [])
        if must_have_reference:
            if references and len(references) > 0:
                # Check if references contain ClinVar ID or PMID
                has_valid_ref = any(
                    'clinvar' in str(ref).lower() or 
                    'pmid' in str(ref).lower() or 
                    re.search(r'\d{6,}', str(ref))  # Looks like an ID
                    for ref in references
                )
                if has_valid_ref:
                    score += 0.75
                else:
                    issues.append("No valid ClinVar/PubMed references found")
            else:
                issues.append("References missing")
        else:
            score += 0.75  # Give credit if references not required
        
        # Pass if score >= 80%
        passed = (score / max_score) >= 0.8
        
        result_msg = f"Score: {score}/{max_score} ({score/max_score*100:.0f}%)"
        if issues:
            result_msg += f"\nIssues: {'; '.join(issues)}"
        
        return passed, result_msg
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON response: {str(e)}"
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func
def validate_treatment_recommendation(llm_response, question: str, expected_therapies: list,
                                       must_include_evidence: bool = True,
                                       check_contraindications: bool = True):
    """
    Validates treatment recommendation response for genomic variants.
    
    Checks:
    - Recommended therapies match expected
    - Evidence level provided (FDA, NCCN, clinical trial)
    - Contraindications checked
    - Dosing considerations included
    """
    try:
        result = llm_response.result if hasattr(llm_response, 'result') else llm_response
        
        if isinstance(result, str):
            data = json.loads(result)
        else:
            data = result
        
        issues = []
        score = 0
        max_score = 4
        
        # 1. Check recommended therapies (40%)
        recommended = data.get('recommended_therapies', [])
        if not isinstance(recommended, list):
            recommended = [recommended] if recommended else []
        
        matched = sum(1 for exp in expected_therapies if any(exp.lower() in str(rec).lower() for rec in recommended))
        if matched >= len(expected_therapies) * 0.7:
            score += 1.6
        else:
            issues.append(f"Therapies: expected {expected_therapies}, got {recommended}")
        
        # 2. Check evidence level (30%)
        if must_include_evidence:
            evidence = data.get('evidence_level', '')
            valid_levels = ['fda', 'nccn', 'clinical trial', 'level 1', 'level 2', 'level a', 'level b']
            if any(level in str(evidence).lower() for level in valid_levels):
                score += 1.2
            else:
                issues.append(f"Evidence level missing or invalid: {evidence}")
        else:
            score += 1.2
        
        # 3. Check contraindications (15%)
        if check_contraindications:
            contraind = data.get('contraindications', [])
            if contraind and len(contraind) > 0:
                score += 0.6
            else:
                issues.append("Contraindications not addressed")
        else:
            score += 0.6
        
        # 4. Check dosing considerations (15%)
        dosing = data.get('dosing', '') or data.get('dosing_considerations', '')
        if dosing and len(str(dosing).strip()) > 10:
            score += 0.6
        else:
            issues.append("Dosing considerations missing or incomplete")
        
        passed = (score / max_score) >= 0.75
        
        result_msg = f"Score: {score}/{max_score} ({score/max_score*100:.0f}%)"
        if issues:
            result_msg += f"\nIssues: {'; '.join(issues)}"
        
        return passed, result_msg
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON response: {str(e)}"
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"


@compare_func
def validate_clinical_trial_match(llm_response, question: str, min_trials: int = 3,
                                   must_check_eligibility: bool = True):
    """
    Validates clinical trial matching response.
    
    Checks:
    - Minimum number of trials found
    - Trial details complete (NCT ID, phase, eligibility)
    - Eligibility criteria assessed
    - Geographic feasibility considered
    """
    try:
        result = llm_response.result if hasattr(llm_response, 'result') else llm_response
        
        if isinstance(result, str):
            data = json.loads(result)
        else:
            data = result
        
        issues = []
        score = 0
        max_score = 4
        
        # 1. Check number of trials (30%)
        trials = data.get('trials', data.get('matched_trials', []))
        if not isinstance(trials, list):
            trials = []
        
        if len(trials) >= min_trials:
            score += 1.2
        else:
            issues.append(f"Expected at least {min_trials} trials, found {len(trials)}")
        
        # 2. Check trial completeness (40%)
        complete_trials = 0
        for trial in trials:
            if isinstance(trial, dict):
                has_nct = 'nct' in str(trial).lower() or 'trial_id' in trial
                has_phase = 'phase' in trial
                has_title = 'title' in trial or 'name' in trial
                if has_nct and has_phase and has_title:
                    complete_trials += 1
        
        if complete_trials >= min_trials * 0.7:
            score += 1.6
        else:
            issues.append(f"Only {complete_trials}/{len(trials)} trials have complete information")
        
        # 3. Check eligibility assessment (20%)
        if must_check_eligibility:
            has_eligibility = any(
                'eligibility' in str(trial).lower() or 
                'eligible' in str(trial).lower()
                for trial in trials
            )
            if has_eligibility:
                score += 0.8
            else:
                issues.append("Eligibility criteria not assessed")
        else:
            score += 0.8
        
        # 4. Check geographic/location info (10%)
        has_location = any(
            'location' in str(trial).lower() or 
            'site' in str(trial).lower() or
            'country' in str(trial).lower()
            for trial in trials
        )
        if has_location:
            score += 0.4
        else:
            issues.append("Location information missing")
        
        passed = (score / max_score) >= 0.75
        
        result_msg = f"Score: {score}/{max_score} ({score/max_score*100:.0f}%)"
        if issues:
            result_msg += f"\nIssues: {'; '.join(issues)}"
        
        return passed, result_msg
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON response: {str(e)}"
    except Exception as e:
        return False, f"Evaluation error: {str(e)}"

