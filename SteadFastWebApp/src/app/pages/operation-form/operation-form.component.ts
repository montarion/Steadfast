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
      name: [''],
      operation: [''],
      author: ['']
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

  getBase64(file: File) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  }

  getBase64EncodedString(file: File) {
    var encoded = "";
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      encoded = reader.result.toString();
    };
    reader.onerror = function (error) {
      console.log('Error: ', error);
    };
    return encoded
  }
  
  // Submit Form
  async submit() {
    if (this.uploadForm.valid && this.uploadForm.get('image').value != null) {
      var totalImageName = this.uploadForm.get('name').value + "." + this.imageExtension
      var operationName = this.uploadForm.get('operation').value
      var author = this.uploadForm.get('author').value
      
      await this.getBase64(this.uploadForm.get('image').value).then(encoded => {
        this.imageBase = encoded.toString();
      })

      if (!this.imageService.ImageNameIsDuplicate(totalImageName)) {
        this.imageService.post(totalImageName, operationName, author, this.imageBase);
      }
      else {
        console.log('Error: ', "this imagename already exists");
        alert("An image with this name already exists, change it's name!")
      }
    }
    else {
      this.formState = "invalid";
      alert('Be sure to fill in all the fields')
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
