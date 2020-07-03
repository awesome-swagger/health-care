import {
  HttpEvent,
  HttpHandler,
  HttpHeaders,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { LocalStorageService } from './storage.service';

@Injectable()
export class AuthTokenInterceptor implements HttpInterceptor {

  constructor(private storage: LocalStorageService) { }

  public intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const authToken = this.storage.getObj('user');
    if (authToken) {
      request = request.clone({
        headers: request.headers.set('Authorization', `Token ${authToken.token}`)
      });
    }
    return next.handle(request);
  }
}
