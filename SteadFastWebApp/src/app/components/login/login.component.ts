import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  alreadyLoggedIn: boolean;
  email: string = '';
  password: string = '';
  
  constructor(private userService: UserService, private router: Router) { }

  ngOnInit() {
    this.userService.user$.subscribe(u => {
      if (u.email !== ""){
        this.alreadyLoggedIn = true;
      } else {
        this.alreadyLoggedIn = false;
      }
    })
  }

  login() {
    if (this.email && this.password) {
      try {
        this.userService.postLogin(this.email.toString(), this.password.toString());
      } catch (Error){
        console.log(Error)
      }
      this.router.navigate(['/home']);
    } else {
      console.log("not everything filled in")
    }
  }


}
