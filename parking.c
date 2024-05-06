#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Parking lot system

typedef struct {
    char license_plate[20];
    int parking_spot;
} Car;

void park_car(Car *car, char *license_plate, int parking_spot) {
    strcpy(car->license_plate, license_plate);
    car->parking_spot = parking_spot;
}

void save_car_info(Car *car) {
    FILE *file = fopen("./data/data.txt", "w");
    if (file == NULL) {
        printf("Unable to open file!\n");
        return;
    }

    fprintf(file, "%s\n%d\n", car->license_plate, car->parking_spot);
    fclose(file);
}

void load_car_info(Car *car) {
    FILE *file = fopen("./data/data.txt", "r");
    if (file == NULL) {
        printf("No previous data found!\n");
        return;
    }

    fscanf(file, "%s\n%d\n", car->license_plate, &car->parking_spot);
    fclose(file);
}

int main(void) {
    Car car;
    char license_plate[20];
    int parking_spot;

    load_car_info(&car);
    printf("Previous car info: License Plate - %s, Parking Spot - %d\n", car.license_plate, car.parking_spot);

    printf("Please park your car!\n");
    printf("License Plate: ");
    scanf("%s", license_plate);
    printf("Parking Spot: ");
    scanf("%d", &parking_spot);

    park_car(&car, license_plate, parking_spot);
    save_car_info(&car);

    printf("Car parked successfully!\n");

    return 0;
}