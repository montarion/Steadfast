import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Image} from '../model/image.model';

@Injectable({
    providedIn: 'root',
})
export class OperationService {

    operationImages: string[] = [];
    baseUrl = "http://83.163.109.161:5000/";
    constructor(private http: HttpClient) {}

    getOperationImages(operation: string){
        return this.http.get<Image>(this.baseUrl + "api/operations/" + operation);
    }

    getOperationNames(){
        return this.http.get<string[]>(this.baseUrl + "api/operations");
    }
}
