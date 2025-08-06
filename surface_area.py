
import os
import re
from pathlib import Path
from niwrap import workbench as wb
import subprocess

def compute_surface_area(input_gifti, output_metric):
    """
    Compute the surface area of a brain surface mesh using niwrap.

    """
    wb.surface_vertex_areas(surface=input_gifti, metric=output_metric)
    print(f"Surface area metric saved to {output_metric}")


def validate_output_file_data(output_metric):
    """
    Validate the output metric file by checking specific data fields.
    """
    try:
        # Basic file existence check
        if not os.path.exists(output_metric):
            print("✗ Output file does not exist")
            return False
            
        file_size = os.path.getsize(output_metric)
        if file_size == 0:
            print("✗ Output file is empty")
            return False
            
        print(f"✓ File exists with size: {file_size} bytes")
        
        # Get file information using subprocess to capture output
        result = subprocess.run(
            ['wb_command', '-file-information', output_metric],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("✗ Failed to get file information")
            return False
            
        output = result.stdout
        print("File information output captured")
        
        # Check for required fields
        required_fields = {
            'Type': 'Metric',
            'Maps to Surface': 'true',
            'Number of Maps': '1',
            'Map Name': 'vertex areas'
        }
        
        validation_results = {}
        
        for field, expected_value in required_fields.items():
            if field == 'Map Name':
                # Special case for map name - check in the table
                pattern = r'vertex areas'
                if re.search(pattern, output, re.IGNORECASE):
                    validation_results[field] = True
                    print(f"✓ {field}: Found 'vertex areas'")
                else:
                    validation_results[field] = False
                    print(f"✗ {field}: 'vertex areas' not found")
            else:
                # Check for field: value pattern
                pattern = f"{field}:\\s*{re.escape(expected_value)}"
                if re.search(pattern, output, re.IGNORECASE):
                    validation_results[field] = True
                    print(f"✓ {field}: {expected_value}")
                else:
                    validation_results[field] = False
                    print(f"✗ {field}: Expected '{expected_value}' not found")
        
        # Check for numeric data fields
        numeric_checks = {
            'Number of Vertices': r'Number of Vertices:\s*(\d+)',
            'Minimum': r'1\s+([\d.]+)',  # Map 1 minimum value
            'Maximum': r'1\s+[\d.]+\s+([\d.]+)',  # Map 1 maximum value
            'Mean': r'1\s+[\d.]+\s+[\d.]+\s+([\d.]+)',  # Map 1 mean value
        }
        
        for check_name, pattern in numeric_checks.items():
            match = re.search(pattern, output)
            if match:
                value = match.group(1)
                try:
                    float_value = float(value)
                    if float_value > 0:
                        validation_results[check_name] = True
                        print(f"✓ {check_name}: {value} (valid positive value)")
                    else:
                        validation_results[check_name] = False
                        print(f"✗ {check_name}: {value} (should be positive)")
                except ValueError:
                    validation_results[check_name] = False
                    print(f"✗ {check_name}: {value} (not a valid number)")
            else:
                validation_results[check_name] = False
                print(f"✗ {check_name}: Not found in output")
        
        # Overall validation result
        all_passed = all(validation_results.values())
        
        if all_passed:
            print("✓ All field validations passed")
        else:
            failed_checks = [k for k, v in validation_results.items() if not v]
            print(f"✗ Failed validations: {', '.join(failed_checks)}")
        
        return all_passed
        
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False

def test_output_file(output_metric):
    """
    Test if the output metric file exists and has valid data fields.
    """
    # First run the niwrap file_information to ensure it works
    try:
        file_info = wb.file_information(output_metric)
        print("✓ niwrap file information executed successfully")
    except Exception as e:
        print(f"✗ niwrap file information failed: {e}")
        return False
    
    # Now validate the actual data fields
    is_valid = validate_output_file_data(output_metric)
    
    if is_valid:
        print("✓ Complete output file validation successful")
    else:
        print("✗ Output file validation failed")
    
    return is_valid

if __name__ == "__main__":
    import glob
    
    # Directory to search for input files
    input_dir = "/home/bshrestha/projects/Tfunck/neuromaps-nhp-prep/share/Inputs"
    
    # Glob for files containing 'mid' or 'midthickness' and ending with .surf.gii
    # Using ** for recursive search through subdirectories
    patterns = [
        os.path.join(input_dir, "**", "*mid*.surf.gii"),
        os.path.join(input_dir, "**", "*midthickness*.surf.gii")
    ]
    
    input_files = []
    for pattern in patterns:
        input_files.extend(glob.glob(pattern, recursive=True))
    
    # Remove duplicates if any
    input_files = list(set(input_files))
    
    if not input_files:
        print("No matching input files found")
        exit(1)
    
    print(f"Found {len(input_files)} input file(s):")
    for input_file in input_files:
        print(f"  - {input_file}")
    
    # Process each input file
    for input_gifti in input_files:
        # Generate output filename by replacing .surf.gii with .func.gii
        # Keep it in the same directory as the input file
        output_metric = input_gifti.replace('.surf.gii', '.func.gii')
        
        print(f"\nProcessing: {os.path.basename(input_gifti)}")
        print(f"Input: {input_gifti}")
        print(f"Output: {output_metric}")
        
        # Run the actual processing
        compute_surface_area(input_gifti, output_metric)
        test_output_file(output_metric)