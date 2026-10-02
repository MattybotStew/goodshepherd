import json

def fix_contact():
    with open("/tmp/contact.json", "r") as f:
        data = f.read()
    
    fixed = data.replace("(555) 123-2222", "(815) 472-3700").replace("(555) 123-2225", "(815) 472-3700")
    
    with open("/tmp/contact_fixed.json", "w") as f:
        f.write(fixed)
    print("Fixed contact phone numbers.")

def fix_careers():
    with open("/tmp/careers.json", "r") as f:
        data = json.load(f)
    
    # Identify the index where "Job Openings" begins
    job_openings_idx = -1
    for i, container in enumerate(data):
        for el in container.get("elements", []):
            if el.get("settings", {}).get("title") == "Job Openings":
                job_openings_idx = i
                break
        if job_openings_idx != -1: break
    
    if job_openings_idx != -1:
        fixed_data = data[job_openings_idx:]
    else:
        # Fallback: filter by keywords
        fixed_data = []
        for container in data:
            container_str = json.dumps(container)
            if any(k in container_str for k in ["Connect with us", "Ways to Give", "Front Office"]):
                continue
            fixed_data.append(container)
            
    with open("/tmp/careers_fixed.json", "w") as f:
        json.dump(fixed_data, f, separators=(",", ":"))
    print("Cleaned careers residue.")

if __name__ == "__main__":
    fix_contact()
    fix_careers()
