using System;
using System.Collections.Generic;

namespace wodehouse
{
    public class FunctionCall : Expression
    {
        public Expression Function;

        public readonly List<Expression> Arguments = new List<Expression>();
    }
}
