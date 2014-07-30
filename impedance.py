def getImpe(f,MaterialInfo,WindingInfo,CoreInfo):
  (sigma,mu0,mur)=MaterialInfo
  (NumofLayer,h,s,w,m)=WindingInfo
  (g,Ae,le,nc,c)=CoreInfo

  d=le*nc #effective length of the winding

  #check length of input matrices
  if NumofLayer!=len(h):
    print 'NumofLayer mismatch with h, please revise #layer or #h'
  if NumofLayer!=len(s):
    print 'NumofLayer mismatch with h\s, please revise #layer or #s'

  for i1 in range(1,NumofLayer+1):
    delta=(2/(f*2*math.pi)/mu0/sigma)**0.5
    Psi=(1+j)/delta
    Z=Psi/sigma
    A=exp(-Psi*h(i1))
    Za=Z*(1-A)/(1+A)
    Zb=Z*2*A/(1-A**2)
    Xa[i1]=d/w[i1]*Za
    Xb[i1]=d/w[i1]*Zb
    Xs[i1]=j*(f*2*math.pi)*mu0*s[i1]*d/w[i1]

    #impedance for the ferrite core
    Xfb=j*(f*2*math.pi)*mu0*Ae/(g+Ae*w[i1]/(mur*c*d))
    Xft=j*(f*2*math.pi)*mu0*mur*c*d/w[i1]

    Ra=real(Xa)
    La=imag(Xa)/(f*2*math.pi)
    Rb=real(Xb)
    Lb=imag(Xb)/(f*2*math.pi)
    Ls=imag(Xs)/(f*2*math.pi)
    Lfb=imag(Xfb)/(f*2*math.pi)
    Lft=imag(Xft)/(f*2*math.pi)

return [Ra,La,Rb,Lb,Ls,Lfb,Lft]
