import { Component, OnInit } from '@angular/core';
import { ImageService } from 'src/app/services/image.service';

@Component({
  selector: 'app-operation-list',
  templateUrl: './operation-list.component.html',
  styleUrls: ['./operation-list.component.scss']
})
export class OperationListComponent implements OnInit {

  image_list: any[] = null;

  constructor(private imageService: ImageService) { }

  ngOnInit() {
    // this.imageService.getImageNamesObservable().subscribe(res => this.image_list = res)
    this.imageService.getFullImageInfos().subscribe(res => {
      var image_names = []
      for (var a of res) {
        image_names.push(a)
      }
      this.image_list = image_names;
    })
  }
}
