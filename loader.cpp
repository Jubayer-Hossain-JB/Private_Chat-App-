// loader.cpp
#include <windows.h>
#include <iostream>
#include <fstream>
#include <vector>

// Function to extract a resource to a file
bool ExtractResourceToFile(int resourceID, const wchar_t* resourceType, const wchar_t* filePath) {
    HRSRC resource = FindResource(NULL, MAKEINTRESOURCE(resourceID), resourceType);
    if (!resource) return false;

    HGLOBAL resourceData = LoadResource(NULL, resource);
    if (!resourceData) return false;

    void* data = LockResource(resourceData);
    if (!data) return false;

    DWORD dataSize = SizeofResource(NULL, resource);

    std::ofstream file(filePath, std::ios::binary);
    if (!file.is_open()) return false;

    file.write(static_cast<const char*>(data), dataSize);
    file.close();

    return true;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Extract logo.png
    wchar_t logoPath[MAX_PATH];
    GetTempPathW(MAX_PATH, logoPath);
    wcscat_s(logoPath, MAX_PATH, L"logo.png");

    if (ExtractResourceToFile(101, L"PNG", logoPath)) { // 101 is the resource ID
        // Display logo (simplified)
        ShellExecuteW(NULL, L"open", logoPath, NULL, NULL, SW_SHOWNORMAL);
    }

    // Extract app.exe
    wchar_t appPath[MAX_PATH];
    GetTempPathW(MAX_PATH, appPath);
    wcscat_s(appPath, MAX_PATH, L"app.exe");

    if (ExtractResourceToFile(102, L"EXE", appPath)) { // 102 is the resource ID
        // Launch app.exe
        ShellExecuteW(NULL, L"open", appPath, NULL, NULL, SW_SHOWNORMAL);
    }

    return 0;
}