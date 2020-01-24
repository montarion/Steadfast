import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  username: string = '';
  email: string = '';
  password: string = '';

  constructor(private userService: UserService, private router: Router) { }

  ngOnInit() {
  }

  register() {
    if (this.email && this.password && this.username) {
      try {
        this.userService.postRegister(this.email.toString(), this.password.toString(), this.username.toString());
      } catch (Error){
        console.log(Error)
      }
      this.router.navigate(['/home']);
      
    } else {
      console.log("not everything filled in")
    }
  }

}
