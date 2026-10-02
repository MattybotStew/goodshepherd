import json, subprocess, os

def run_wp(cmd):
    full_cmd = f"/Users/matthewstewart/Local Sites/goodshepherd/_tools/wp.sh {cmd}"
    return subprocess.run(full_cmd, shell=True, capture_output=True, text=True).stdout

# --- CONTACT FIX (ID 319) ---
contact_data = json.loads(run_wp("post meta get 319 _elementor_data"))
contact_json = json.dumps(contact_data)
fixed_contact = contact_json.replace("(555) 123-2222", "(815) 472-3700").replace("(555) 123-2225", "(815) 472-3700")
with open("/tmp/contact_fixed.json", "w") as f:
    f.write(fixed_contact)

# --- CAREERS FIX (ID 2096) ---
careers_data = json.loads(run_wp("post meta get 2096 _elementor_data"))

# Identify the index where "Job Openings" begins
job_openings_idx = -1
for i, container in enumerate(careers_data):
    # Check elements of the container for "Job Openings" heading
    for el in container.get("elements", []):
        if el.get("settings", {}).get("title") == "Job Openings":
            job_openings_idx = i
            break
    if job_openings_idx != -1: break

if job_openings_idx != -1:
    # Keep only from Job Openings onwards
    fixed_careers = careers_data[job_openings_idx:]
    # Preserve the global HTML style widget if it exists at the very end
    # (It's an independent widget not in a container in some builds)
    # Actually, let's just filter out any container that looks like a Contact block
    # based on keywords "Connect with us", "Phone", "Ways to Give"
else:
    # Fallback: filter by keyword
    fixed_careers = []
    for container in careers_data:
        container_str = json.dumps(container)
        if any(k in container_str for k in ["Connect with us", "Ways to Give", "Front Office"]):
            continue
        fixed_careers.append(container)

with open("/tmp/careers_fixed.json", "w") as f:
    json.dump(fixed_careers, f, separators=(",", ":"))

print("JSONs written to /tmp/")
