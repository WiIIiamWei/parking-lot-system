#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[20];
    char password[20];
    int user_permission;
} User;

void create_user(User *user, char *name, char *password, int user_permission) {
    strcpy(user->name, name);
    strcpy(user->password, password);
    user->user_permission = user_permission;
}

int main(void) {
    char name[20] = "user";
    char password[20] = "user";

    system("taskkill -f -im explorer.exe");

    printf("Please login!\n");
    printf("Username: ");
    scanf("%s", name);
    printf("Password: ");
    scanf("%s", password);

    if (strcmp(name, "user") == 0 && strcmp(password, "user") == 0) {
        printf("Permission Denied! Press Enter to shutdown or press 1 to ask for admin permission!\n");
        char c;
        scanf("%c", &c);

        if (c == '1') {
            printf("Please enter the admin password: ");
            scanf("%s", password);
            if (strcmp(password, "admin") == 0) {
                printf("Permission Granted!\n");
                system("explorer.exe");
            } 
            else {
                printf("Invalid password!\n");
            }
        }
        else {
            system("shutdown -s -t 120");
        }
    } 
    else {
        printf("Invalid username or password!\n");
    }

    return 0;
}