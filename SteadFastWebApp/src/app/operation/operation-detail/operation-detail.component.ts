import { Component, OnInit, Input } from '@angular/core';
import { ImageService } from 'src/app/services/image-service';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-operation-detail',
  templateUrl: './operation-detail.component.html',
  styleUrls: ['./operation-detail.component.scss']
})
export class OperationDetailComponent implements OnInit {

  constructor(private route: ActivatedRoute, private imageService: ImageService) { }
  operation: string;
  image_list: string[] = []

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.operation = params['id'];
      this.imageService.getOperationImageNames(this.operation).subscribe(res => {
        this.image_list = res;
      },
        err => {
          console.log(err);
        });
    });
  }
}
