import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export class ImageService {

    existingImages: string[] = []
    baseUrl = "localhost:5000/"
    constructor(private http: HttpClient) {
        this.getImageNames()
    }

    ImageNameIsDuplicate(nameToCheck: string) {
        this.getImageNames();
        if (this.existingImages.includes(nameToCheck)) {
            return true;
        }
        this.existingImages.push(nameToCheck)
        return false;
    }

    getImageNames() {
        this.http.get<string[]>(this.baseUrl + "api/images").subscribe(res => {
            this.existingImages = res;
        })
    }

    post(imageName, baseEncoded) {
        this.http.post((this.baseUrl + "api/images"), {
            "image-name": imageName,
            "base-encoded-image": baseEncoded
        })
    }

}