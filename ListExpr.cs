using System;
using System.Collections.Generic;

namespace wodehouse
{
    public class ListExpr : Expression
    {
        public readonly List<Expression> Expressions = new List<Expression>();
    }
}
