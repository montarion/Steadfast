import { Component, OnInit, OnDestroy } from '@angular/core';
import { UserService } from 'src/app/services/user.service';
import { Observable, Subscription } from 'rxjs';
import { User } from 'src/app/model/user.model';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  user: User = null;

  constructor(private userService: UserService) {
  }

  getUser() {
    return this.userService.getCurrentUser();
  }

  ngOnInit() {
    this.userService.user$.subscribe(loggedInUser => {
      console.log('loggedinuser', loggedInUser)
      if (Object.keys(loggedInUser).length == 0) {
        this.user = null;
      }
      if (loggedInUser.email == "" && loggedInUser.username == "")
        this.user = null;
      else {
        this.user = loggedInUser;
      }
    })
  }

  logOut() {
    this.userService.logOut();
  }
}
