import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export class ImageService {

    existingImages: string[] = []
    baseUrl = 'http://0.0.0.0:5000/' //"http://83.163.109.161/"
    constructor(private http: HttpClient) {
        // this.getImageNames()
    }

    ImageNameIsDuplicate(nameToCheck: string) {
        // this.getImageNames();
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
        var json = JSON.stringify({
            "image_name": imageName,
            "operation_name": "test-operation",
            "author": "test-author",
            "image_info": {
                "path_to_file": ""
            },
            "comments": [],
            "base_encoded_image": baseEncoded
        })
        try {
            this.http.post((this.baseUrl + "api/images"), json).subscribe(res => console.log(res))
            console.log(json)
        } catch (error) {
            alert(error)
        }

    }

}