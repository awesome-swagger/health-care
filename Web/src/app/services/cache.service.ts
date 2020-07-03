import { HttpRequest, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable()
export class CacheService {

  private cache: any = [];

  public get(request: HttpRequest<any>): HttpResponse<any> | null {
    // Check if the cache contains this request
    let cached = this.cache.find((cachedRequest) => {
      return request.urlWithParams === cachedRequest.request.urlWithParams;
    });
    // If so, return the response for the request, if not return null
    if (cached) {
      return cached.response;
    }
    return null;
  }

  public put(request: HttpRequest<any>, response: HttpResponse<any>): void {
    // Check if the cache contains this request
    let cachedIndex = this.cache.findIndex((cachedRequest) => {
      return request.urlWithParams === cachedRequest.request.urlWithParams;
    });
    // If there is a cached version, update it, if not, add it
    if (cachedIndex !== -1) {
      this.cache[cachedIndex].response = response;
    } else {
      this.cache.push({
        request: request,
        response: response,
      });
    }
  }
}
