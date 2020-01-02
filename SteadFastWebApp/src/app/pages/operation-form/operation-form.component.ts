import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ImageService } from 'src/app/services/image-service';

@Component({
  selector: 'app-operation-form',
  templateUrl: './operation-form.component.html',
  styleUrls: ['./operation-form.component.scss']
})
export class OperationFormComponent implements OnInit {

  imageExtension: string;
  imageURL: string;
  imageBase: string;
  uploadForm: FormGroup;
  formState: string = "valid";
  constructor(private http: HttpClient, public fb: FormBuilder, private imageService: ImageService) {
    this.uploadForm = this.fb.group({
      image: [null],
      name: ['']
    })
  }

  ngOnInit() { }

  showPreview(event) {
    const file = (event.target as HTMLInputElement).files[0];
    this.uploadForm.patchValue({
      image: file
    });
    this.uploadForm.get('image').updateValueAndValidity()

    var filenameParts = file.name.split('.')
    this.imageExtension = filenameParts[filenameParts.length - 1];
    // File Preview
    const reader = new FileReader();
    reader.onload = () => {
      this.imageURL = reader.result as string;
    }
    reader.readAsDataURL(file)
  }

  // Submit Form
  submit() {
    if (this.uploadForm.valid) {
      var totalImageName = this.uploadForm.get('name').value + "." + this.imageExtension
      let reader = new FileReader();
      reader.readAsDataURL(this.uploadForm.get('image').value);
      reader.onload = () => {
        this.imageBase = reader.result.toString();
      };
      reader.onerror = function (error) {
        console.log('Error: ', error);
      };

      if (this.imageService.ImageNameIsDuplicate(totalImageName)) {
        console.log('Error: ', "this imagename already exists");
        alert('An image with this name already exists, change it!')
      }

      this.imageService.post(totalImageName, this.imageBase);
    }
    else {
      this.formState = "invalid";
    }
  }

  // onSubmit() {
  //   const formData = new FormData();
  //   formData.append('file', this.fileData);
  //   let reader = new FileReader();
  //   reader.readAsDataURL(this.fileData);
  //   reader.onload = () => {
  //     console.log(reader.result);
  //     this.baseImage = reader.result.toString();
  //   };
  //   reader.onerror = function (error) {
  //     console.log('Error: ', error);
  //   };
  //   alert('succes!')
  // }
}
