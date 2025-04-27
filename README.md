## Bulk User Story Creator for Azure DevOps

This script allows you to **bulk create User Stories** in **Azure DevOps** automatically from a **CSV file**.

- Each User Story can include:
  - Title (`Title`)
  - Description (`Description`)
  - Acceptance Criteria (`AcceptanceCriteria`)
  - Direct association to a **Feature** (`FeatureID`)

- The script connects through the **Azure DevOps REST API** using a **Personal Access Token (PAT)** for secure authentication.

- It is ideal for quickly and consistently loading large batches of user stories into new projects or during backlog migrations.

---

# 📦 Requirements

- Python 3.x
- `requests` Python package
- A **Personal Access Token (PAT)** with `Work Items (Read and Write)` permissions in Azure DevOps.

---

# 🚀 How to Use

1. Configure your `settings.json` file with your organization, project, and token.
2. Prepare your `user_stories.csv` file using the following format:
   ```csv
   Title,Description,FeatureID,AcceptanceCriteria
   ```
3. Run the script:

   ```bash
   python create_user_stories.py
   ```

4. Done! Each User Story will be created and automatically linked to the specified Feature.
