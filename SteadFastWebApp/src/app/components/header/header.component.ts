import { Component, OnInit, OnDestroy } from '@angular/core';
import { UserService } from 'src/app/services/user.service';
import { Observable, Subscription } from 'rxjs';
import { User } from 'src/app/model/user.model';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit, OnDestroy {

  user: User = null;
  subscription: Subscription;

  constructor(private userService: UserService) {
    this.subscription = this.userService.getUser().subscribe(user => {
      this.user = user;
    })
  }

  getUser(): Observable<User> {
    return this.userService.user$.asObservable();
  }

  ngOnInit() {
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }
}
