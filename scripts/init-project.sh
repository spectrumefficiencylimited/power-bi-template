#!/bin/bash

# PBIP Project Initialisation Script
# Usage: ./scripts/init-project.sh "Project Name"

set -e

# Colours for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Colour

# Check if project name provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Project name required${NC}"
    echo "Usage: ./scripts/init-project.sh \"Project Name\""
    echo "Example: ./scripts/init-project.sh \"Student Enrollment Dashboard\""
    exit 1
fi

PROJECT_NAME="$1"
# Convert to PascalCase for folder names (remove spaces, capitalise words)
FOLDER_NAME=$(echo "$PROJECT_NAME" | sed 's/ //g')

echo -e "${GREEN}Initialising PBIP project: ${PROJECT_NAME}${NC}"
echo "Folder name: ${FOLDER_NAME}"
echo ""

# Check if we're in the template root
if [ ! -f "Project.Template.pbip" ]; then
    echo -e "${RED}Error: Must run from repository root (where Project.Template.pbip exists)${NC}"
    exit 1
fi

# Check if already initialised
if [ -f "${FOLDER_NAME}.pbip" ] && [ "$FOLDER_NAME" != "Project.Template" ]; then
    echo -e "${YELLOW}Warning: ${FOLDER_NAME}.pbip already exists.${NC}"
    read -p "Continue and overwrite? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "Aborted."
        exit 0
    fi
fi

echo "Step 1: Renaming PBIP pointer file..."
if [ -f "Project.Template.pbip" ]; then
    # Update the content to reference new folder names
    sed "s/Project\.Template/${FOLDER_NAME}/g" Project.Template.pbip > "${FOLDER_NAME}.pbip"
    rm -f Project.Template.pbip
    echo -e "  ${GREEN}✓${NC} Created ${FOLDER_NAME}.pbip"
fi

echo "Step 2: Renaming Report folder..."
if [ -d "Project.Template.Report" ]; then
    mv "Project.Template.Report" "${FOLDER_NAME}.Report"
    echo -e "  ${GREEN}✓${NC} Renamed to ${FOLDER_NAME}.Report"
fi

echo "Step 3: Renaming SemanticModel folder..."
if [ -d "Project.Template.SemanticModel" ]; then
    mv "Project.Template.SemanticModel" "${FOLDER_NAME}.SemanticModel"
    echo -e "  ${GREEN}✓${NC} Renamed to ${FOLDER_NAME}.SemanticModel"
fi

echo "Step 4: Updating report.json..."
REPORT_JSON="${FOLDER_NAME}.Report/definition/report.json"
if [ -f "$REPORT_JSON" ]; then
    sed -i.bak "s/Project Template Report/${PROJECT_NAME}/g" "$REPORT_JSON"
    sed -i.bak "s/Template report - rename and configure for your project/${PROJECT_NAME} - Power BI Report/g" "$REPORT_JSON"
    rm -f "${REPORT_JSON}.bak"
    echo -e "  ${GREEN}✓${NC} Updated report.json"
fi

echo "Step 5: Updating model.tmdl..."
MODEL_TMDL="${FOLDER_NAME}.SemanticModel/definition/model.tmdl"
if [ -f "$MODEL_TMDL" ]; then
    sed -i.bak "s/Template semantic model/${PROJECT_NAME} Semantic Model/g" "$MODEL_TMDL"
    rm -f "${MODEL_TMDL}.bak"
    echo -e "  ${GREEN}✓${NC} Updated model.tmdl"
fi

echo "Step 6: Updating metadata files..."
# Update Project Overview with project name
OVERVIEW="docs/01_ProjectOverview.md"
if [ -f "$OVERVIEW" ]; then
    sed -i.bak "s/_\[Enter report name\]_/${PROJECT_NAME}/g" "$OVERVIEW"
    rm -f "${OVERVIEW}.bak"
    echo -e "  ${GREEN}✓${NC} Updated 01_ProjectOverview.md"
fi

echo "Step 7: Updating README..."
if [ -f "README.md" ]; then
    # Add project-specific note at the top
    TEMP_README=$(mktemp)
    echo "# ${PROJECT_NAME}" > "$TEMP_README"
    echo "" >> "$TEMP_README"
    echo "> This project was created from the PBIP Metadata Template." >> "$TEMP_README"
    echo "" >> "$TEMP_README"
    echo "---" >> "$TEMP_README"
    echo "" >> "$TEMP_README"
    cat README.md >> "$TEMP_README"
    mv "$TEMP_README" README.md
    echo -e "  ${GREEN}✓${NC} Updated README.md"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Project initialisation complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Open ${FOLDER_NAME}.pbip in Power BI Desktop"
echo "  2. Add your data sources and build your model"
echo "  3. Complete the metadata documentation in /docs"
echo "  4. Commit your changes:"
echo ""
echo "     git add ."
echo "     git commit -m \"Initial setup: ${PROJECT_NAME}\""
echo ""
echo -e "${YELLOW}Remember to enable PBIP preview features in Power BI Desktop:${NC}"
echo "  File → Options → Preview features → Enable PBIP and PBIR"
echo ""
