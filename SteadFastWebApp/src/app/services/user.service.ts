import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Observable, Subject, BehaviorSubject } from 'rxjs';
import { User } from '../model/user.model';
import { map ,  distinctUntilChanged } from 'rxjs/operators';
import { JwtHelper } from './jwt.helper';

@Injectable({
    providedIn: 'root',
})
export class UserService {
    authToken: string = null;

    private currentUserSubject = new BehaviorSubject<User>({} as User);
    public user$ = this.currentUserSubject.asObservable().pipe(distinctUntilChanged());

    baseUrl = 'http://83.163.109.161:5000/';

    constructor(private http: HttpClient, private cookieService: CookieService, private jwtHelper: JwtHelper) {
        let tokenExists = this.cookieService.check('sf-auth-token');
        if (tokenExists) {
            this.authToken = this.cookieService.get('sf-auth-token');
            let tokenJson = this.jwtHelper.decodeToken(this.authToken);
            this.currentUserSubject.next({ username: tokenJson['usr'], email: tokenJson['sub'] });
            console.log("Next User:", { username: tokenJson['usr'], email: tokenJson['sub'] });
        } else {
            console.log("no cookie set yet")
            this.currentUserSubject.next({ username: "", email: "" });
        }
    }

    postRegister(email: string, password: string, username: string) {
        this.http.post(this.baseUrl + 'api/register', { email: email, password: password, username: username })
            .subscribe(
                res => {
                    console.log(res)
                    this.cookieService.set('sf-auth-token', res['auth_token']);

                    let tokenJson = this.jwtHelper.decodeToken(res['auth_token']);

                    this.currentUserSubject.next({ username: tokenJson['usr'], email: tokenJson['sub'] });
                },
                err => {
                    console.log(err);
                }
            );
    }

    postLogin(email: string, password: string) {
        this.http.post(this.baseUrl + 'api/login', { email: email, password: password })
            .subscribe(
                res => {
                    console.log(res)
                    this.cookieService.set('sf-auth-token', res['auth_token']);
                    let tokenJson = this.jwtHelper.decodeToken(res['auth_token']);

                    this.currentUserSubject.next({ username: tokenJson['usr'], email: tokenJson['sub'] });
                },
                err => {
                    console.log(err)
                });
    }

    logOut() {
        this.cookieService.delete('sf-auth-token');
        this.currentUserSubject.next({ username: "", email: "" });
    }

    getCurrentUserInfoFromApi() {
        if (this.authToken) {
            this.http.get(this.baseUrl + 'api/user', { headers: { 'Authorization': 'Bearer' + this.authToken } })
        } else {
            console.log("This request will fail. Login first.")
        }
    }

    getCurrentUser(): User {
        return this.currentUserSubject.value;
      }
}
