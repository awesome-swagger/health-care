import {
  HttpEvent,
  HttpHandler,
  HttpHeaders,
  HttpInterceptor,
  HttpResponse,
  HttpRequest,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { CacheService } from './cache.service';

@Injectable()
export class CacheInterceptor implements HttpInterceptor {

  constructor(private cache: CacheService) { }

  public intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // If not a get request, continue as normal
    if (request.method !== 'GET') {
      return next.handle(request);
    }
    // If there is a cached response, return it
    const cachedResponse = this.cache.get(request);
    if (cachedResponse) {
      // console.log('used cached version!');
      return Observable.of(cachedResponse);
    }
    // If not handle the request as normal, but add it to the cache
    return next.handle(request).do((event) => {
      if (event instanceof HttpResponse) {
        this.cache.put(request, event);
      }
    });
  }
}
