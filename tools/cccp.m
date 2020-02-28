function [X, T] = cccp(RB, Y, I, K, R, r, y, x,w) 

mu=1000;
% Define x(i) as a column vector (I,1)
% Define R(i) as a column vector (I,1)
% Define Y
% [y_1,....y_J], where y_j=[col_1:col_2]; (start,end).
% b(k)=r(k)
% K urllc user number
% X in (K,R).
% I EMBB USERS.

% sliding window A INITIALIZATION
% for k=1:K
% A(:,:,k)=zeros(R,R-r(k)+1);
% for i=1:R-r(k)+1
%     
%     a=[ones(r(k),1);zeros(R-r(k),1)];
%     for j=1:R
%         A(:,j,k)=a(1:R);
%         a=[0;a];
%     end
% end
% end

%lambda>0
XX=zeros(K,RB);
a=1;
flag=1;
memory=[];
delta=0.1;
while a == 1 
clear t;
cvx_begin
    variables X(K,RB);
    
    for k=1:K
        ones(1,RB)*X(k,:)'==r(k);
    end

    
    for k1=1:I
    harm=sum(sum(X(:,y(k1,1):y(k1,2))));
    t(k1,1)=(1-harm/R(k1))*x(k1);
    t(k1,1)=log(t(k1,1));
    t(k1,1)=w(k1)*t(k1,1);
    end
    
    for k1=1:K
        for k2=1:RB
            0<=X(k1,k2)<=1;
        end
    end

    for k=1:RB
       ones(1,K)*X(:,k)<=1;
    end
    
    minimize -1*ones(1,I)*t-mu*sum(sum( (2*XX.^2-ones(K,RB)).*(X-XX) )) % +sum(sum(lambda*.s))
    
cvx_end
XX = X;
memory=cat(3,memory,XX);

if flag>=5 && abs(-1*ones(1,I)*t-mu*sum(sum( (2*memory(:,:,flag-1).^2-ones(K,RB)).*(memory(:,:,flag-2)-memory(:,:,flag-1)))) - (-1*ones(1,I)*t-mu*sum(sum( (2*memory(:,:,flag-2).^2-ones(K,RB)).*(memory(:,:,flag-3)-memory(:,:,flag-2)))))) <=delta
    break;
end
flag=flag+1;
end

%output X
    for k1=1:I
    harm=sum(sum(X(:,y(k1,1):y(k1,2))));
    T(k1,1)=(1-harm/R(k1))*x(k1);
    end

end

