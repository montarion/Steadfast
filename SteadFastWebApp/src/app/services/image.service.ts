import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export class ImageService {

    existingImages: string[] = [];
    baseUrl = "http://83.163.109.161:5000/";
    constructor(private http: HttpClient) {
        this.getImageNames();
    }

    ImageNameIsDuplicate(nameToCheck: string) {
        this.getImageNames();
        if (this.existingImages.includes(nameToCheck)) {
            return true;
        }
        return false;
    }

    getImageNamesObservable() {
        // tslint:disable-next-line: quotemark
        return this.http.get<string[]>(this.baseUrl + "api/images");
    }

    getImageNames() {
        this.http.get<string[]>(this.baseUrl + "api/images").subscribe(res => {
            this.existingImages = res;
        })
    }

    getOperationImageNames(operation_name: string) {
        return this.http.get<string[]>(this.baseUrl + "api/operations/" + operation_name)
    }

    getFullImageInfos(){
        return this.http.get<string[]>(this.baseUrl + "api/images/operations")
    }

    post(imageName: string, operationName: string, author: string, baseEncoded: string) {
        var json = JSON.stringify({
            "image_name": imageName,
            "operation_name": operationName,
            "author": author,
            "image_info": {
                "path_to_file": ""
            },
            "comments": [],
            "base_encoded_image": baseEncoded
        });
        this.http.post((this.baseUrl + "api/images"), json).subscribe(
            res => {
                this.existingImages.push(imageName);
                alert("Added "+imageName+" to the wall");
            },
            error => {
                console.log('error', error);
                alert('Something went wrong, try again!');
            }
        );
    }
}
