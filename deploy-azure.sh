#!/bin/bash

# Azure Container Deployment Script for Pytest UI Framework
# This script automates the deployment of the containerized test framework to Azure

set -e

# Configuration
RESOURCE_GROUP_NAME="pytest-ui-framework-rg"
LOCATION="eastus"
DEPLOYMENT_NAME="pytest-ui-deployment-$(date +%Y%m%d-%H%M%S)"
SUBSCRIPTION_ID=""  # Set your subscription ID
CONTAINER_IMAGE_TAG="pytest-ui-framework:latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Azure CLI is installed
check_azure_cli() {
    if ! command -v az &> /dev/null; then
        print_error "Azure CLI is not installed. Please install it first."
        exit 1
    fi
    print_status "Azure CLI found"
}

# Function to check if user is logged in
check_azure_login() {
    if ! az account show &> /dev/null; then
        print_warning "Not logged in to Azure. Attempting to log in..."
        az login
    fi
    print_status "Logged in to Azure"
}

# Function to set subscription
set_subscription() {
    if [ -n "$SUBSCRIPTION_ID" ]; then
        print_status "Setting subscription to $SUBSCRIPTION_ID"
        az account set --subscription "$SUBSCRIPTION_ID"
    else
        print_warning "No subscription ID specified. Using default subscription."
    fi
}

# Function to create resource group
create_resource_group() {
    print_status "Creating resource group: $RESOURCE_GROUP_NAME"
    az group create \
        --name "$RESOURCE_GROUP_NAME" \
        --location "$LOCATION" \
        --output table
}

# Function to build and push Docker image to ACR
build_and_push_image() {
    print_status "Building Docker image locally..."
    docker build -t "$CONTAINER_IMAGE_TAG" .
    
    # Get ACR login server (will be created during deployment)
    print_status "Docker image built successfully"
}

# Function to validate Bicep template
validate_deployment() {
    print_status "Validating Bicep template..."
    az deployment group validate \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --template-file infra/main.bicep \
        --parameters infra/main.parameters.json \
        --output table
    
    print_status "Template validation successful"
}

# Function to preview deployment changes
preview_deployment() {
    print_status "Previewing deployment changes..."
    az deployment group what-if \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --template-file infra/main.bicep \
        --parameters infra/main.parameters.json \
        --name "$DEPLOYMENT_NAME"
}

# Function to deploy to Azure
deploy_to_azure() {
    print_status "Deploying to Azure..."
    az deployment group create \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --template-file infra/main.bicep \
        --parameters infra/main.parameters.json \
        --name "$DEPLOYMENT_NAME" \
        --output table
    
    print_status "Deployment completed successfully"
}

# Function to get deployment outputs
get_deployment_outputs() {
    print_status "Getting deployment outputs..."
    az deployment group show \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$DEPLOYMENT_NAME" \
        --query properties.outputs \
        --output table
}

# Function to push image to ACR after deployment
push_to_acr() {
    print_status "Getting ACR login server..."
    ACR_LOGIN_SERVER=$(az deployment group show \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$DEPLOYMENT_NAME" \
        --query properties.outputs.containerRegistryLoginServer.value \
        --output tsv)
    
    if [ "$ACR_LOGIN_SERVER" != "external" ]; then
        print_status "Logging in to ACR: $ACR_LOGIN_SERVER"
        az acr login --name "${ACR_LOGIN_SERVER%%.azurecr.io}"
        
        print_status "Tagging and pushing image to ACR..."
        docker tag "$CONTAINER_IMAGE_TAG" "$ACR_LOGIN_SERVER/$CONTAINER_IMAGE_TAG"
        docker push "$ACR_LOGIN_SERVER/$CONTAINER_IMAGE_TAG"
        
        print_status "Image pushed to ACR successfully"
    else
        print_warning "Using external registry, skipping ACR push"
    fi
}

# Function to trigger test run
trigger_test_run() {
    print_status "Triggering test run in container..."
    CONTAINER_GROUP_NAME=$(az deployment group show \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$DEPLOYMENT_NAME" \
        --query properties.outputs.containerGroupName.value \
        --output tsv)
    
    # Restart container group to run tests
    az container restart \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$CONTAINER_GROUP_NAME"
    
    print_status "Test run triggered. Monitor logs with:"
    echo "az container logs --resource-group $RESOURCE_GROUP_NAME --name $CONTAINER_GROUP_NAME --follow"
}

# Function to show test results URL
show_results_url() {
    BLOB_URL=$(az deployment group show \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$DEPLOYMENT_NAME" \
        --query properties.outputs.blobContainerUrl.value \
        --output tsv)
    
    print_status "Test results will be available at: $BLOB_URL"
}

# Function to cleanup resources
cleanup() {
    read -p "Do you want to delete the resource group $RESOURCE_GROUP_NAME? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Deleting resource group..."
        az group delete --name "$RESOURCE_GROUP_NAME" --yes --no-wait
        print_status "Resource group deletion initiated"
    fi
}

# Main execution
main() {
    print_status "Starting Azure Container Deployment for Pytest UI Framework"
    
    # Pre-flight checks
    check_azure_cli
    check_azure_login
    set_subscription
    
    # Create infrastructure
    create_resource_group
    validate_deployment
    
    # Ask user if they want to preview changes
    read -p "Do you want to preview deployment changes? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        preview_deployment
    fi
    
    # Confirm deployment
    read -p "Proceed with deployment? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        deploy_to_azure
        get_deployment_outputs
        
        # Build and push if using ACR
        build_and_push_image
        push_to_acr
        
        # Trigger test run
        trigger_test_run
        show_results_url
        
        print_status "Deployment completed successfully!"
        print_status "Monitor your test execution and results in the Azure Portal"
        
        # Offer cleanup option
        echo
        cleanup
    else
        print_warning "Deployment cancelled by user"
    fi
}

# Run main function
main "$@"