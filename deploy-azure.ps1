# PowerShell Azure Deployment Script for Pytest UI Framework
# Windows-compatible version of the deployment script

param(
    [string]$ResourceGroupName = "pytest-ui-framework-rg",
    [string]$Location = "eastus", 
    [string]$SubscriptionId = "",
    [string]$ContainerImageTag = "pytest-ui-framework:latest",
    [switch]$Preview,
    [switch]$Cleanup
)

# Colors for output
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

# Generate deployment name with timestamp
$DeploymentName = "pytest-ui-deployment-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

function Test-AzureCLI {
    try {
        az --version | Out-Null
        Write-Status "Azure CLI found"
        return $true
    }
    catch {
        Write-Error "Azure CLI is not installed. Please install it first."
        return $false
    }
}

function Test-AzureLogin {
    try {
        az account show | Out-Null
        Write-Status "Logged in to Azure"
        return $true
    }
    catch {
        Write-Warning "Not logged in to Azure. Attempting to log in..."
        az login
        return $true
    }
}

function Set-AzureSubscription {
    if ($SubscriptionId) {
        Write-Status "Setting subscription to $SubscriptionId"
        az account set --subscription $SubscriptionId
    }
    else {
        Write-Warning "No subscription ID specified. Using default subscription."
    }
}

function New-ResourceGroup {
    Write-Status "Creating resource group: $ResourceGroupName"
    az group create --name $ResourceGroupName --location $Location --output table
}

function Test-BicepTemplate {
    Write-Status "Validating Bicep template..."
    az deployment group validate `
        --resource-group $ResourceGroupName `
        --template-file "infra/main.bicep" `
        --parameters "infra/main.parameters.json" `
        --output table
    
    Write-Status "Template validation successful"
}

function Show-DeploymentPreview {
    Write-Status "Previewing deployment changes..."
    az deployment group what-if `
        --resource-group $ResourceGroupName `
        --template-file "infra/main.bicep" `
        --parameters "infra/main.parameters.json" `
        --name $DeploymentName
}

function Start-AzureDeployment {
    Write-Status "Deploying to Azure..."
    az deployment group create `
        --resource-group $ResourceGroupName `
        --template-file "infra/main.bicep" `
        --parameters "infra/main.parameters.json" `
        --name $DeploymentName `
        --output table
    
    Write-Status "Deployment completed successfully"
}

function Get-DeploymentOutputs {
    Write-Status "Getting deployment outputs..."
    az deployment group show `
        --resource-group $ResourceGroupName `
        --name $DeploymentName `
        --query "properties.outputs" `
        --output table
}

function Build-DockerImage {
    Write-Status "Building Docker image locally..."
    docker build -t $ContainerImageTag .
    Write-Status "Docker image built successfully"
}

function Push-ToACR {
    Write-Status "Getting ACR login server..."
    $AcrLoginServer = az deployment group show `
        --resource-group $ResourceGroupName `
        --name $DeploymentName `
        --query "properties.outputs.containerRegistryLoginServer.value" `
        --output tsv
    
    if ($AcrLoginServer -ne "external") {
        Write-Status "Logging in to ACR: $AcrLoginServer"
        $AcrName = ($AcrLoginServer -split '\.')[0]
        az acr login --name $AcrName
        
        Write-Status "Tagging and pushing image to ACR..."
        docker tag $ContainerImageTag "$AcrLoginServer/$ContainerImageTag"
        docker push "$AcrLoginServer/$ContainerImageTag"
        
        Write-Status "Image pushed to ACR successfully"
    }
    else {
        Write-Warning "Using external registry, skipping ACR push"
    }
}

function Start-TestRun {
    Write-Status "Triggering test run in container..."
    $ContainerGroupName = az deployment group show `
        --resource-group $ResourceGroupName `
        --name $DeploymentName `
        --query "properties.outputs.containerGroupName.value" `
        --output tsv
    
    # Restart container group to run tests
    az container restart `
        --resource-group $ResourceGroupName `
        --name $ContainerGroupName
    
    Write-Status "Test run triggered. Monitor logs with:"
    Write-Host "az container logs --resource-group $ResourceGroupName --name $ContainerGroupName --follow" -ForegroundColor Cyan
}

function Show-ResultsURL {
    $BlobUrl = az deployment group show `
        --resource-group $ResourceGroupName `
        --name $DeploymentName `
        --query "properties.outputs.blobContainerUrl.value" `
        --output tsv
    
    Write-Status "Test results will be available at: $BlobUrl"
}

function Remove-Resources {
    if ($Cleanup) {
        $Confirm = Read-Host "Do you want to delete the resource group $ResourceGroupName? (y/N)"
        if ($Confirm -eq 'y' -or $Confirm -eq 'Y') {
            Write-Status "Deleting resource group..."
            az group delete --name $ResourceGroupName --yes --no-wait
            Write-Status "Resource group deletion initiated"
        }
    }
}

# Main execution
function Main {
    Write-Status "Starting Azure Container Deployment for Pytest UI Framework"
    
    # Pre-flight checks
    if (-not (Test-AzureCLI)) { return }
    if (-not (Test-AzureLogin)) { return }
    Set-AzureSubscription
    
    # Create infrastructure
    New-ResourceGroup
    Test-BicepTemplate
    
    # Preview changes if requested
    if ($Preview) {
        Show-DeploymentPreview
    }
    
    # Confirm deployment
    $Proceed = Read-Host "Proceed with deployment? (y/N)"
    if ($Proceed -eq 'y' -or $Proceed -eq 'Y') {
        Start-AzureDeployment
        Get-DeploymentOutputs
        
        # Build and push Docker image
        Build-DockerImage
        Push-ToACR
        
        # Trigger test run
        Start-TestRun
        Show-ResultsURL
        
        Write-Status "Deployment completed successfully!"
        Write-Status "Monitor your test execution and results in the Azure Portal"
        
        # Cleanup option
        Remove-Resources
    }
    else {
        Write-Warning "Deployment cancelled by user"
    }
}

# Run main function
Main