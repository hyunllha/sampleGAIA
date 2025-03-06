# create_project_structure.ps1

# Directory structure definition
$structure = @{
    "core" = @{
        "config" = @("settings.py", "constants.py")
        "logger" = @("logger.py")
    }
    "security" = @{
        "credentials" = @("api_keys.py", "auth.py")
        "encryption" = @("cipher.py", "keys.py")
        "policies" = @("constants.py")
    }
    "services" = @{
        "ai" = @("claude.py", "processor.py")
        "translator" = @("translator.py")
    }
    "templates" = @("loader.py", "manager.py")
    "cs" = @{
        "workflow" = @("onestep.py", "twostep.py")
        "responses" = @("generator.py")
    }
    "utils" = @{
        "validators" = @("template.py", "response.py", "common.py")
        "formatters" = @("text.py", "response.py")
    }
    "ui" = @{
        "static" = @{
            "css" = @{
                "components" = @()
            }
            "js" = @{
                "modules" = @()
            }
            "images" = @()
        }
        "templates" = @{
            "components" = @()
            "pages" = @()
        }
    }
    "data" = @{
        "templates" = @()
    }
}

# Function to create directories and files
function Create-Structure {
    param (
        [string]$basePath,
        [object]$structure
    )
    
    foreach ($key in $structure.Keys) {
        $path = Join-Path $basePath $key
        New-Item -ItemType Directory -Force -Path $path
        
        # Create __init__.py for Python packages
        if ($path -notmatch "static|templates|data|images|components|pages|modules") {
            New-Item -ItemType File -Force -Path (Join-Path $path "__init__.py")
        }
        
        # Create CSS files
        if ($key -eq "css") {
            New-Item -ItemType File -Force -Path (Join-Path $path "main.css")
        }
        
        # Create JavaScript files
        if ($key -eq "js") {
            New-Item -ItemType File -Force -Path (Join-Path $path "main.js")
        }
        
        # Create HTML template files
        if ($key -eq "templates" -and $basePath -match "ui$") {
            New-Item -ItemType File -Force -Path (Join-Path $path "base.html")
        }
        
        if ($structure[$key] -is [array]) {
            foreach ($file in $structure[$key]) {
                New-Item -ItemType File -Force -Path (Join-Path $path $file)
            }
        }
        elseif ($structure[$key] -is [hashtable]) {
            Create-Structure -basePath $path -structure $structure[$key]
        }
    }
}

# Execute structure creation
Create-Structure -basePath "." -structure $structure

Write-Host "Project structure has been created successfully."