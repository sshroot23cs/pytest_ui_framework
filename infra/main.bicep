# Azure Container Instance Configuration for Pytest UI Framework
# This file defines the Azure infrastructure for deploying the test framework

targetScope = 'resourceGroup'

@description('Name prefix for all resources')
param namePrefix string = 'pytest-ui'

@description('Location for all resources')
param location string = resourceGroup().location

@description('Container image to deploy')
param containerImage string = 'pytestui:latest'

@description('Container registry server')
param registryServer string = ''

@description('Container registry username')
@secure()
param registryUsername string = ''

@description('Container registry password')
@secure()
param registryPassword string = ''

@description('Environment for deployment (dev/test/prod)')
@allowed(['dev', 'test', 'prod'])
param environment string = 'dev'

// Variables
var resourceBaseName = '${namePrefix}-${environment}'
var containerGroupName = '${resourceBaseName}-container-group'
var containerName = 'pytest-ui-framework'

// Azure Container Registry (if needed)
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = if (empty(registryServer)) {
  name: '${replace(resourceBaseName, '-', '')}acr'
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}

// Storage Account for test results and reports
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: '${replace(resourceBaseName, '-', '')}storage'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: true
  }
}

// Blob Container for test reports
resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/test-reports'
  properties: {
    publicAccess: 'Blob'
  }
}

// Log Analytics Workspace for monitoring
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${resourceBaseName}-logs'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// Container Group for running pytest tests
resource containerGroup 'Microsoft.ContainerInstance/containerGroups@2023-05-01' = {
  name: containerGroupName
  location: location
  properties: {
    containers: [
      {
        name: containerName
        properties: {
          image: empty(registryServer) ? containerRegistry.properties.loginServer + '/' + containerImage : '${registryServer}/${containerImage}'
          resources: {
            requests: {
              cpu: 2
              memoryInGB: 4
            }
          }
          environmentVariables: [
            {
              name: 'AZURE_STORAGE_ACCOUNT'
              value: storageAccount.name
            }
            {
              name: 'AZURE_STORAGE_KEY'
              secureValue: storageAccount.listKeys().keys[0].value
            }
            {
              name: 'ENVIRONMENT'
              value: environment
            }
            {
              name: 'HEADLESS'
              value: 'true'
            }
            {
              name: 'CHROME_ARGS'
              value: '--no-sandbox --disable-dev-shm-usage --disable-gpu --remote-debugging-port=9222'
            }
          ]
          volumeMounts: [
            {
              name: 'test-results'
              mountPath: '/app/reports'
            }
          ]
        }
      }
    ]
    osType: 'Linux'
    restartPolicy: 'OnFailure'
    imageRegistryCredentials: empty(registryServer) ? [
      {
        server: containerRegistry.properties.loginServer
        username: containerRegistry.name
        password: containerRegistry.listCredentials().passwords[0].value
      }
    ] : [
      {
        server: registryServer
        username: registryUsername
        password: registryPassword
      }
    ]
    volumes: [
      {
        name: 'test-results'
        azureFile: {
          shareName: 'test-results'
          storageAccountName: storageAccount.name
          storageAccountKey: storageAccount.listKeys().keys[0].value
        }
      }
    ]
    diagnostics: {
      logAnalytics: {
        workspaceId: logAnalytics.properties.customerId
        workspaceKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

// File Share for persistent test results
resource fileShare 'Microsoft.Storage/storageAccounts/fileServices/shares@2023-01-01' = {
  name: '${storageAccount.name}/default/test-results'
  properties: {
    shareQuota: 100
  }
}

// Outputs
output containerGroupName string = containerGroup.name
output storageAccountName string = storageAccount.name
output containerRegistryName string = empty(registryServer) ? containerRegistry.name : 'external'
output containerRegistryLoginServer string = empty(registryServer) ? containerRegistry.properties.loginServer : registryServer
output logAnalyticsWorkspaceId string = logAnalytics.properties.customerId
output blobContainerUrl string = 'https://${storageAccount.name}.blob.core.windows.net/test-reports'