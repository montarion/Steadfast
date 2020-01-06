import { Component, OnInit } from '@angular/core';
import { ImageService } from 'src/app/services/image-service';

@Component({
  selector: 'app-operation-list',
  templateUrl: './operation-list.component.html',
  styleUrls: ['./operation-list.component.scss']
})
export class OperationListComponent implements OnInit {

  image_list: string[] = []

  constructor(private imageService: ImageService) { }

  ngOnInit() {
    this.imageService.getImageNamesObservable().subscribe(res => this.image_list = res)
    console.log(this.image_list)
  }
}
